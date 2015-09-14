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

PORTAL_TYPES = ["reg","game","lboard"]

def name_to_bool(name):
	if name=="open": return True
	elif name=="close": return False
	else: return None

def bool_to_name(is_open):
	if is_open: return "open"
	else: return "closed"

def set_status(portal_type,is_open):
	if portal_type in PORTAL_TYPES:
		try:
			gk = User.objects.get(username=portal_type+"_gatekeeper")
		except User.DoesNotExist:
			gk = User(username=portal_type+"_gatekeeper",is_staff=True)
			gk.set_unusable_password()
		gk.is_active = (not is_open)
		gk.save()

def set_all(is_open):
	for portal_type in PORTAL_TYPES:
		set_status(portal_type,is_open)

def get_status(portal_type):
	if portal_type in PORTAL_TYPES:
		try:
			gk = User.objects.get(username=portal_type+"_gatekeeper")
			return not gk.is_active
		except User.DoesNotExist:
			return True

def print_all():
	for portal_type in PORTAL_TYPES:
		status = get_status(portal_type)
		print(portal_type,": ",bool_to_name(status),sep='')

if __name__=="__main__":
	import sys
	args = sys.argv[1:]
	if len(args)==0:
		print_all()
	elif len(args)==1:
		is_open = name_to_bool(args[0])
		if is_open==True or is_open==False:
			set_all(is_open)
			print("All portals",bool_to_name(is_open))
		elif args[0] in PORTAL_TYPES:
			status = get_status(args[0])
			print(args[0],": ",bool_to_name(status),sep='')
		else:
			print("Invalid first argument")
	else:
		is_open = name_to_bool(args[1])
		if args[0] not in PORTAL_TYPES:
			print("Invalid first argument")
		elif is_open!=True and is_open!=False:
			print("Invalid second argument")
		else:
			set_status(args[0],is_open)
			print_all()
