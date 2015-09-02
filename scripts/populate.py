import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
	sys.path.append(BASE_DIR)

DEFAULT_QUESTIONS_FILE_PATH = os.path.join(BASE_DIR, "data", "questions.json")

import json

def get_dist(lat1,long1,lat2,long2):
	return 0

def add_data_from_file(file_path):
	ques_dict = json.load(open(file_path))
	for loc_name, ques in ques_dict.items():
		db_ques = Question(loc_name=loc_name)
		fields = ('answer','rent','stipend')
		db_ques.text = ques.get('question','')
		for field in fields:
			if field in ques:
				setattr(db_ques,field,ques[field])
		db_ques.save()
	for source_name, source_data in ques_dict.items():
		if "latitude" in source_data and "longitude" in source_data:
			for dest_name, dest_data in ques_dict.items():
				if "latitude" in dest_data and "longitude" in dest_data:
					dist = get_dist(source_data["latitude"], source_data["longitude"], dest_data["latitude"], dest_data["longitude"])
					source_db_obj = Question.objects.get(loc_name=source_name)
					dest_db_obj = Question.objects.get(loc_name=dest_name)
					Distance(source=source_db_obj, dest=dest_db_obj, distance=dist).save()

if __name__=="__main__":
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'checkmate.settings')
	print("Setting up Django...")
	import django
	django.setup()

from main.models import Question, Distance

if __name__=="__main__":
	add_data_from_file(DEFAULT_QUESTIONS_FILE_PATH)
