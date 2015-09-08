"""
Lists all users who have made multiple accounts from same IP address
"""

import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
	sys.path.append(BASE_DIR)

if __name__=="__main__":
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'checkmate.settings')
	print("Setting up Django...")
	import django
	django.setup()

from main.models import Player
import json
from pprint import pprint

def get_cheaters():
	players = list(Player.objects.order_by('ip_address').values_list('user__username','ip_address','score'))
	if len(players)<=1:
		return []
	cheaters = []
	if players[0][1]==players[1][1]:
		cheaters.append(players[0])
	if players[-1][1]==players[-2][1]:
		cheaters.append(players[-1])
	for i in range(1,len(players)-1):
		if players[i-1][1]==players[i][1] or players[i+1][1]==players[i][1]:
			cheaters.append(players[i])
	return cheaters

if __name__=="__main__":
#	print(json.dumps(get_cheaters(),indent=2))
	pprint(get_cheaters())
