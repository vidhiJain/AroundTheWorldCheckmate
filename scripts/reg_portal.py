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

from django.contrib.auth.models import User

def reg_portal_open(switch):
	try:
		gk = User.objects.get(username="gatekeeper")
	except User.DoesNotExist:
		gk = User(username="gatekeeper",is_staff=True)
		gk.set_unusable_password()
	gk.is_active = (not switch)
	gk.save()

if __name__=="__main__":
	import sys
	if len(sys.argv)!=2:
		print('This script takes exactly 1 commmand line argument ("open" or "close")')
	else:
		arg = sys.argv[1].lower()
		if arg=="open":
			reg_portal_open(True)
		elif arg=="close":
			reg_portal_open(False)
		else:
			print('The command line argument has to be one of ["open","close"]')
