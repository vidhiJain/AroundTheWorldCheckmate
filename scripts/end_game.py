import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
	sys.path.append(BASE_DIR)

from django.utils import timezone

def end_game():
	User.objects.exclude(username__in=["admin","gatekeeper"]).update(is_active=False)
	# a single database query makes sure that the game ends for everyone at the same time
	reg_portal_open(False)
	now = timezone.now()
	for player in Player.objects.filter(curr_loc__isnull=False):
		player.fly_to(None,now)
		player.save()

if __name__=="__main__":
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'checkmate.settings')
	print("Setting up Django...")
	import django
	django.setup()

from django.contrib.auth.models import User
from main.models import Player, Distance
from django.conf import settings
from scripts import reg_portal_open

if __name__=="__main__":
	end_game()
