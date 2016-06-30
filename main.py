import json
from sentence_corrector import main
from wit_get_reply_api import interpret_wit_output, get_entities_json_wit
from user_features import updateUser
from interpret_wit_reply import getFeatures
from getFilters import wit_extract_filters
from applyFilters import getProjects
# from map_recommendation import nextFeatureSuggestion
from mapProjectsToUser import sortProjects
from map_user_n_question import get_suggestions

if __name__ == '__main__':
	user = "prirqlxu"
	message = 'I want a  house in which we should have tennis and servant room with area less than 1200 sq.ft.'
	message =  main(message) # spell correct
	# print message
	# message = 'I want a house in which we should have tennis and servant room with price greater than 1200 rs'
	entities = get_entities_json_wit(message) #this is json object of entities from wit.
	# msg_features = get_entities_from_msg_Wit(message)
	# print msg_features
	dict_features = interpret_wit_output(entities) #structure derived from wit reply.
	# print dict_features
	# print json.dumps(entities,indent = 4)
	# print dict_features
	user_ft =  getFeatures(dict_features) # extract user features to be used from wit reply
	updateUser(user,user_ft) #updated user features in elastic search
	filters = wit_extract_filters(dict_features) #extract filters from wit reply
	# print filters
	project_list = getProjects(filters, user) #
	print project_list
	# project_list_sorted = sortProjects(project_list, user)
	# print project_list_sorted
	# print msg_features

	print get_suggestions(user, 'buy')
