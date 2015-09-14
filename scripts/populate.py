import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
	sys.path.append(BASE_DIR)

DEFAULT_QUESTIONS_FILE_PATH = os.path.join(BASE_DIR, "data", "questions.json")

import json
import math

def square(n):
	return n*n

def get_dist(phi1,phi2,dlmd):
	sinp1 = math.sin(phi1*math.pi/180.0)
	sinp2 = math.sin(phi2*math.pi/180.0)
	sindl = math.sin(dlmd*math.pi/180.0)
	cosp1 = math.cos(phi1*math.pi/180.0)
	cosp2 = math.cos(phi2*math.pi/180.0)
	cosdl = math.cos(dlmd*math.pi/180.0)
	num = math.sqrt(square(cosp2*sindl)+square(cosp1*sinp2-sinp1*cosp2*cosdl))
	den = sinp1*sinp2+cosp1*cosp2*cosdl
	return settings.CONFIG["earth_radius_in_km"] * math.atan2(num,den)

def set_data_from_file(file_path):
	ques_dict = json.load(open(file_path))
	print("Loading locations...")
	Question.objects.all().delete()
	User.objects.exclude(player__isnull=True).delete()
	for loc_name, ques in ques_dict.items():
		db_ques = Question(loc_name=loc_name)
		fields = ('answer','rent','stipend')
		db_ques.text = ques.get('question','')
		for field in fields:
			if field in ques:
				setattr(db_ques,field,ques[field])
		db_ques.save()
	print("Precomputing distances...")
	Distance.objects.all().delete()
	for source_name, source_data in ques_dict.items():
		if "latitude" in source_data and "longitude" in source_data:
			for dest_name, dest_data in ques_dict.items():
				if "latitude" in dest_data and "longitude" in dest_data:
					if dest_name==source_name:
						dist=0
					else:
						dist = get_dist(source_data["latitude"], dest_data["latitude"], abs(source_data["longitude"] - dest_data["longitude"]))
					source_db_obj = Question.objects.get(loc_name=source_name)
					dest_db_obj = Question.objects.get(loc_name=dest_name)
					Distance(source=source_db_obj, dest=dest_db_obj, distance=dist).save()

if __name__=="__main__":
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'checkmate.settings')
	print("Setting up Django...")
	import django
	django.setup()

from main.models import Question, Distance
from django.contrib.auth.models import User
from django.conf import settings

if __name__=="__main__":
	set_data_from_file(DEFAULT_QUESTIONS_FILE_PATH)
