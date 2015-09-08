"""
mfl - Make Frontend Locations
This file takes questions.json and returns the corresponding locations.json
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEFAULT_QUESTIONS_FILE_PATH = os.path.join(BASE_DIR, "data", "questions.json")
DEFAULT_LOCATIONS_FILE_PATH = os.path.join(BASE_DIR, "static", "data", "locations.json")
DEFAULT_JSONP_LOCATIONS_FILE_PATH = os.path.join(BASE_DIR, "static", "data", "locations.js")

REQUIRED_FIELDS = ('latitude','longitude')
OPTIONAL_FIELDS = ('country','rent','stipend')

import json
from collections import OrderedDict

def make_loc_file():
	loc_dict = OrderedDict()
	try:
		os.mkdir(os.path.join(BASE_DIR, "static", "data"))
	except FileExistsError:
		pass
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

	loc_string = json.dumps(loc_dict, indent=2)

	json_file = open(DEFAULT_LOCATIONS_FILE_PATH,'w')
	json_file.write(loc_string)
	json_file.close()
	js_file = open(DEFAULT_JSONP_LOCATIONS_FILE_PATH,'w')
	js_file.write("var locations = "+loc_string)
	js_file.close()


if __name__=="__main__":
	make_loc_file()
