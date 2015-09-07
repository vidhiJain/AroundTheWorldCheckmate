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

if __name__=="__main__":
	print("Creating superusers...")
	try: User.objects.get(username="admin").delete()
	except User.DoesNotExist: pass
	try: User.objects.get(username="gatekeeper").delete()
	except User.DoesNotExist: pass
	admin,created = User.objects.get_or_create(username="admin",password="admin",is_active=True,is_staff=True,is_superuser=True)
	admin.set_password(admin.password)
	admin.save()
	gk = User(username="gatekeeper",password="gatekeeper",is_active=True,is_staff=True,is_superuser=False)
	gk.set_password(gk.password)
	gk.save()
