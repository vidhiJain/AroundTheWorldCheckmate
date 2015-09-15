from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.http import require_safe
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder

from . import models, forms

import os
import json
from base64 import b64decode
from collections import OrderedDict
from datetime import timedelta, datetime
from django.utils import timezone
from django.conf import settings

from scripts import status

def TextResponse(message, status=None):
	return HttpResponse(message, content_type="text/plain", status=status)

def MyJsonResponse(object_to_send, status=None):
	return HttpResponse(json.dumps(object_to_send, indent=settings.JSON_INDENT_LEVEL, cls=DjangoJSONEncoder), content_type="application/json", status=status)

def get_user_from_auth_header(request):
	"""
	Uses the authentication header to get a username and password
	and then fetches the user object from the database
	If authentication was successful, returns (user,"success")
	else returns (None,auth_status_code)

	Possible auth status codes and their meanings:
	auth_missing: Authorization header is not present
	invalid_auth: Authorization header is corrupt
	unsupported_auth: Non-basic auth was used. Only basic auth is supported
	wrong_login: The username or password is incorrect
	success: The supplied credentials are correct
	"""
	header = request.META.get('HTTP_AUTHORIZATION')
	if not header:
		return (None,"auth_missing")
	header_parts = header.split()
	if len(header_parts)!=2:
		return (None,"invalid_auth")
	auth_type, digest = header_parts
	if auth_type.lower()!='basic':
		return (None,"unsupported_auth")
	try:
		smashed_credentials = b64decode(digest.encode('utf-8')).decode('utf-8')
	except Exception:
		return (None,"invalid_auth")
	credentials = smashed_credentials.split(':',maxsplit=1)
	if len(credentials)!=2:
		return (None,"invalid_auth")
	username, password = credentials
	user = authenticate(username=username,password=password)
	if not user:
		return (None,"wrong_login")
	elif not status.get_status("game"):
		return (user,"game_closed")
	elif user.is_active:
		return (user,"success")
	else:
		return (user,"inactive")

def basic_auth_required(function):
	# This is a decorator
	def wrapper(request,*args,**kwargs):
		user, auth_status_code = get_user_from_auth_header(request)
		if user:
			request.user = user
			if auth_status_code=="success":
				return function(request,*args,**kwargs)
			else:
				return TextResponse(auth_status_code, status=403)
		else:
			return TextResponse(auth_status_code, status=401)
	return wrapper

def enable_CORS(method):
	# This is a decorator
	def outer_wrapper(function):
		def inner_wrapper(request,*args,**kwargs):
			if request.method=='OPTIONS':
				response = TextResponse('')
				response['Access-Control-Allow-Methods'] = method
				response['Access-Control-Allow-Headers'] = "Authorization"
			elif request.method==method:
				response = function(request,*args,**kwargs)
			else:
				return HttpResponse('',content_type='text/plain',status=405)
			response['Access-Control-Allow-Origin'] = '*'
			return response
		return inner_wrapper
	return outer_wrapper

@csrf_exempt
@enable_CORS('POST')
def register(request):
	"""
	Content-Type: text/plain

	Possible error messages and their meanings:
	invalid_data: The form did not pass backend validation checks. form.is_valid() returned False
	username_taken: The username supplied for registration is already in use
	success: The account was successfully created
	"""
	if not status.get_status("reg"):
		return TextResponse("reg_closed")

	form = forms.PlayerForm(request.POST)
	if not form.is_valid():
		return TextResponse("invalid_data", status=400)

	player = form.save(commit=False)
	username = form.cleaned_data["username"]
	password = form.cleaned_data["password"]
	if User.objects.filter(username=username).exists():
		return TextResponse("username_taken")
	user = User(username=username)
	user.set_password(password)
	user.save()
	player.user = user

	player.score = settings.CONFIG["initial_score"]
	loc_name = settings.CONFIG.get("initial_location")
	if loc_name:
		try:
			player.curr_loc = models.Question.objects.get(loc_name=loc_name)
		except models.Question.DoesNotExist:
			print(loc_name,"does not exist")
	player.arrival_time = timezone.now()
	player.ip_address = request.META["REMOTE_ADDR"]
	player.save()

	return TextResponse("success")

@enable_CORS('GET')
@basic_auth_required
def check_user(request):
	return TextResponse("success")

@enable_CORS('GET')
def user_status(request):
	user, auth_status_code = get_user_from_auth_header(request)
	if not user:
		return TextResponse(auth_status_code, status=401)
	player = user.player
	d = OrderedDict()
	d["is_active"] = user.is_active
	d["score"] = player.score
	if settings.DEBUG:
		d["dyn_score"] = player.dyn_score()
		d["arrival_time"] = player.arrival_time
	d["stay_duration"] = (timezone.now()-player.arrival_time).total_seconds()
	attempts_left = player.attempts_left()
	if attempts_left!=None:
		d["attempts_left"] = attempts_left
	if player.curr_loc:
		d["curr_loc"] = player.curr_loc.loc_name
		d["question"] = player.curr_loc.text
	else:
		d["curr_loc"] = None
		d["question"] = ""
	return MyJsonResponse(d)

@csrf_exempt
@enable_CORS('POST')
@basic_auth_required
def exit_game(request):
	player = request.user.player
	player.fly_to(None,timezone.now())
	player.save()
	player.user.is_active = False
	player.user.save()
	r = {"score":player.score}
	return JsonResponse(r)

@require_safe
def lboard(request):
	if status.get_status('lboard'):
		qset = models.Player.objects.order_by('-score')[:settings.CONFIG['lboard_size']]
		name_score_list = list(qset.values_list('user__username','score'))
		response = MyJsonResponse(name_score_list)
	else:
		response = TextResponse('Leaderboard is closed',status=403)
	response['Access-Control-Allow-Origin'] = '*'
	return response

@require_safe
def site_status(request):
	response_dict = OrderedDict()
	for portal_type in status.PORTAL_TYPES:
		response_dict[portal_type] = status.get_status(portal_type)
	response = MyJsonResponse(response_dict)
	response['Access-Control-Allow-Origin'] = '*'
	return response

@csrf_exempt
@enable_CORS('POST')
@basic_auth_required
def fly_to(request):
	loc_name = request.body.decode('utf-8')
	player = request.user.player
	try:
		new_loc = models.Question.objects.get(loc_name=loc_name)
	except models.Question.DoesNotExist:
		err_str = "cannot fly to unknown location "+loc_name
		return JsonResponse({"error":err_str})
	player.fly_to(new_loc,timezone.now())
	player.save()

	response_dict = OrderedDict()
	response_dict["score"] = player.score
	attempts_left = player.attempts_left()
	if attempts_left!=None:
		response_dict["attempts_left"] = attempts_left
	response_dict["question"] = new_loc.text
	return MyJsonResponse(response_dict)

@csrf_exempt
@enable_CORS('POST')
@basic_auth_required
def submit(request):
	player = request.user.player
	user_answer = request.body.decode('utf-8')
	response_dict = OrderedDict()
	response_dict["attempt_status"] = player.submit(user_answer)
	attempts_left = player.attempts_left()
	if attempts_left!=None:
		response_dict["attempts_left"] = attempts_left
	response_dict["score"] = player.score
	return MyJsonResponse(response_dict)

@enable_CORS('GET')
@basic_auth_required
def loc_distr(request):
	# gives a list of cities which are passive, correct, wrong1 (not attemptable), wrong2 (attemptable)
	response_dict = OrderedDict()
	user = request.user
	max_attempts = settings.CONFIG["max_attempts_per_question"]
	response_dict["correct"] = list(models.Attempt.objects.filter(user=user,correct=True).values_list("question__loc_name",flat=True))
	response_dict["blocked"] = list(models.Attempt.objects.filter(user=user,correct=False,attempts__gte=max_attempts).values_list("question__loc_name",flat=True))
	response_dict["wrong"] = list(models.Attempt.objects.filter(user=user,correct=False,attempts__lt=max_attempts).values_list("question__loc_name",flat=True))
	return MyJsonResponse(response_dict)
