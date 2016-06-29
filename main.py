import json
from sentence_corrector import main
from wit_get_reply_api import *
from user_features import *
from interpret_wit_reply import *
from getFilters import *
from applyFilters import *
from map_recommendation import nextFeatureSuggestion

if __name__ == '__main__':
	message = 'I want a house in which we should have tennis and servant room with price greater than 1200 rs'
	message =  main(message)
	message = 'I want a house in which we should have tennis and servant room with price less than 1200 rs'
	entities = get_entities_json_wit(message) #this is json object of entities from wit.
	msg_features = get_entities_from_msg_Wit(message)
	# print msg_features
	
	dict_features = interpret_wit_output(entities)
	# print dict_features
	# print json.dumps(entities,indent = 4)
	# print dict_features
	# user_ft =  getFeatures(dict_features)
	# updateUser('ddgpsaqf',user_ft)
	filters = wit_extract_filters(dict_features)
	# print filters
	print getProjects(filters)
	print msg_features