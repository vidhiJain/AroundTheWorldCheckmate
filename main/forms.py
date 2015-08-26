from django import forms
from main.models import Player
from django.contrib.auth.models import User

class PlayerForm(forms.ModelForm):
	username = forms.CharField(required=True, validators=User._meta.get_field('username').validators)
	password = forms.CharField(required=True, validators=User._meta.get_field('password').validators)
	class Meta:
		model = Player
		fields = Player.contact_fields
