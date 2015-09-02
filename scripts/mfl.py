"""
mfl - Make Frontend Locations
This file takes questions.json and returns the corresponding locations.json
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEFAULT_QUESTIONS_FILE_PATH = os.path.join(BASE_DIR, "data", "questions.json")
DEFAULT_LOCATIONS_FILE_PATH = os.path.join(BASE_DIR, "static", "locations.json")

REQUIRED_FIELDS = ('latitude','longitude')
OPTIONAL_FIELDS = ('country','rent','stipend')

import json
from collections import OrderedDict

def make_loc_file():
	loc_dict = OrderedDict()
	with open(DEFAULT_QUESTIONS_FILE_PATH) as _ques_file:
		try:
			ques_dict = json.load(_ques_file, object_pairs_hook=OrderedDict)
		except ValueError as v:
			print("The input file is not a valid JSON file")
			print("Here are the details of the error:")
			print(v)
			return
		for loc_name, ques in ques_dict.items():
			valid_ques = True

			details_dict = OrderedDict()
			for key in REQUIRED_FIELDS:
				if key in ques:
					details_dict[key] = ques[key]
				else:
					valid_ques = False
					break
			if not valid_ques:
				continue

			for key in OPTIONAL_FIELDS:
				if key in ques:
					details_dict[key] = ques[key]
			loc_dict[loc_name] = details_dict

	json.dump(loc_dict, open(DEFAULT_LOCATIONS_FILE_PATH,'w'), indent=2)

if __name__=="__main__":
	make_loc_file()
