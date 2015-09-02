"""
mfl - Make Frontend Locations
This file takes questions.json and returns the corresponding locations.json
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEFAULT_QUESTIONS_FILE_PATH = os.path.join(BASE_DIR, "data", "questions.json")
DEFAULT_LOCATIONS_FILE_PATH = os.path.join(BASE_DIR, "static", "locations.json")

REQUIRED_FIELDS_TO_COPY = ('latitude','longitude','rent','stipend')
OPTIONAL_FIELDS_TO_COPY = ('country',)
REQUIRED_FIELDS_TO_LEAVE = ('question','answer')

def generate_slug(s):
	return s.replace(' ','_').lower()

import json
from collections import OrderedDict

def make_loc_file():
	loc_dict = OrderedDict()
	with open(DEFAULT_QUESTIONS_FILE_PATH) as _ques_file:
		ques_list = json.load(_ques_file, object_pairs_hook=OrderedDict)
		for loc_name, ques in ques_list.items():
			valid_ques = True

			for key in REQUIRED_FIELDS_TO_LEAVE:
				if key not in ques:
					valid_ques = False
					break
			if not valid_ques:
				continue

			details_dict = OrderedDict()
			for key in REQUIRED_FIELDS_TO_COPY:
				if key in ques:
					details_dict[key] = ques[key]
				else:
					valid_ques = False
					break
			if not valid_ques:
				continue

			for key in OPTIONAL_FIELDS_TO_COPY:
				if key in ques:
					details_dict[key] = ques[key]
			loc_dict[loc_name] = details_dict

	json.dump(loc_dict, open(DEFAULT_LOCATIONS_FILE_PATH,'w'), indent=2)

if __name__=="__main__":
	make_loc_file()
