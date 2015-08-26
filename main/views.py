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

def status_and_message(status, message):
	response_dict = OrderedDict()
	response_dict["status"] = status
	response_dict["message"] = message
	return HttpResponse(json.dumps(response_dict, indent=2), content_type="application/json")

@require_POST
@csrf_exempt
def register(request):
	form = forms.PlayerForm(request.POST)
	if not form.is_valid():
		return status_and_message("invalid_data", "The form did not pass backend validation checks. form.is_valid() returned False")

	player = form.save(commit=False)
	username = form.cleaned_data["username"]
	password = form.cleaned_data["password"]
	if User.objects.filter(username=username).exists():
		return status_and_message("user_taken", "The username \'"+username+"\' is already in use")
	user = User(username=username)
	user.set_password(password)
	user.save()
	player.user = user

	player.score = settings.CONFIG.get("initial_score")
	loc_name = settings.CONFIG.get("initial_location")
	if loc_name:
		try:
			player.curr_loc = models.Question.objects.get(loc_name=loc_name)
		except models.Question.DoesNotExist:
			pass
	player.save()

	return status_and_message("success", "The username \'"+username+"\' was successfully registered")

def check_user(request):
	header = request.META.get('HTTP_AUTHORIZATION')
	if not header:
		return status_and_message("no_auth","Authorization header is not present")
	header_parts = header.split()
	corrupt_header_response = status_and_message("invalid_auth","Authorization header is corrupt")
	if len(header_parts)!=2:
		return corrupt_header_response
	auth_type, digest = header_parts
	if auth_type.lower()!='basic':
		return status_and_message("unsupported_auth", "This auth type is not supported. Only basic auth is supported")
	credentials = b64decode(digest.encode('utf-8')).decode('utf-8').split(':',maxsplit=1)
	if len(credentials)!=2:
		return corrupt_header_response
	username, password = credentials
	user = authenticate(username=username,password=password)
	if not user:
		return status_and_message("wrong_login", "The username or password is incorrect")
	else:
		return status_and_message("success", "The supplied credentials are correct")
	return HttpResponse(username+':'+password, content_type='text/plain')
