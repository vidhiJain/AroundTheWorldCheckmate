from django.http import HttpResponse, JsonResponse
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.http import require_http_methods, require_safe, require_POST
from django.views.decorators.csrf import csrf_exempt

from . import models, forms

import os
import json
from base64 import b64decode
from collections import OrderedDict
from datetime import timedelta, datetime
from django.utils import timezone
from django.conf import settings

def TextResponse(message, status=None):
	return HttpResponse(message, content_type="text/plain", status=status)

@require_POST
@csrf_exempt
def register(request):
	"""
	Content-Type: text/plain

	Possible error messages and their meanings:
	invalid_data: The form did not pass backend validation checks. form.is_valid() returned False
	username_taken: The username supplied for registration is already in use
	success: The account was successfully created
	"""
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

	player.score = settings.CONFIG.get("initial_score")
	loc_name = settings.CONFIG.get("initial_location")
	if loc_name:
		try:
			player.curr_loc = models.Question.objects.get(loc_name=loc_name)
			player.arrival_time= timezone.now()
		except models.Question.DoesNotExist:
			print(loc_name,"does not exist")
	player.save()

	return TextResponse("success")

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
	else:
		return (user,"success")

def basic_auth_required(function):
	# This is a decorator
	def wrapper(request,*args,**kwargs):
		user, auth_status_code = get_user_from_auth_header(request)
		if user:
			request.user = user
			return function(request,*args,**kwargs)
		else:
			return TextResponse(auth_status_code, status=401)
	return wrapper

@basic_auth_required
def check_user(request):
	return TextResponse("success")
