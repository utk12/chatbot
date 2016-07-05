from flask import Blueprint, jsonify
from flask_restful import reqparse
from jsonmerge import merge
import json
import sys
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

from sentence_corrector import spell_correct
from wit_get_reply_api import interpret_wit_output, get_entities_json_wit
from user_features import updateUser
from interpret_wit_reply import getFeatures
from getFilters import wit_extract_filters
from applyFilters import getProjects
from mapProjectsToUser import sortProjects
from map_user_n_question import get_suggestions
from tools import *
chat_blueprint = Blueprint('chat_blueprint', __name__)

@chat_blueprint.route('/chatbot')
def post():
	parser = reqparse.RequestParser()
	parser.add_argument('msg', type=str)
	parser.add_argument('id', type=str)
	parser.add_argument('operation', type=str)
	parser.add_argument('filters', type=str)

	args = parser.parse_args()
	message = args['msg']
	user = args['id']
	operation = args['operation']
	previous_filters = json.loads(args['filters'])
	# return "Yo"
	message =  spell_correct(message) # spell correct
	entities = get_entities_json_wit(message) #this is json object of entities from wit.
	dict_features = interpret_wit_output(entities) #structure derived from wit reply.
	user_ft =  getFeatures(dict_features) # extract user features to be used from wit reply
	updateUser(user,user_ft) #updated user features in elastic search
	filters = wit_extract_filters(dict_features) #extract filters from wit reply
	filters_n1 = to_camelcase(filters)
	# -------------
	filters_n2 = merge(previous_filters, filters_n1)
	filters_n3 = to_underscore(filters_n2)
	project_list = getProjects(filters_n3, user)
	suggestions = get_suggestions(user, operation)
	return  jsonify({"projects" :  project_list, "suggestions" : suggestions, "filters" : filters_n2})


if __name__ == '__main__':
	message = "I want a house in sohna road"
	user = "-KLV8E4Rx1pTdMs0G2di"
	operation = "buy"
	message =  spell_correct(message) # spell correct
	entities = get_entities_json_wit(message) #this is json object of entities from wit.
	dict_features = interpret_wit_output(entities) #structure derived from wit reply.
	# user_ft =  getFeatures(dict_features) # extract user features to be used from wit reply
	# updateUser(user,user_ft) #updated user features in elastic search
	print dict_features
	filters = wit_extract_filters(dict_features) #extract filters from wit reply
	print filters
	filters_n1 = to_camelcase(filters)
	# -------------
	# filters_n2 = merge(previous_filters, filters_n1)
	filters_n3 = to_underscore(filters_n1)
	project_list = getProjects(filters_n3, user)
	print project_list
	suggestions = get_suggestions(user, operation)
	print  json.dumps({"projects" :  project_list, "suggestions" : suggestions, "filters" : filters_n1})