import json
from sentence_corrector import main
from wit_get_reply_api import *
from user_features import *
from interpret_wit_reply import *
from getFilters import *
from applyFilters import *
from map_recommendation import nextFeatureSuggestion

if __name__ == '__main__':
	message = 'I want an apartment in which we should have football and vrv'
	message =  main(message)
	entities = get_entities_json_wit(message) #this is json object of entities from wit.
	msg_features = get_entities_from_msg_Wit(message)

	dict_features = interpret_wit_output(entities)
	print dict_features
	# print json.dumps(entities,indent = 4)
	# print dict_features
	# user_ft =  getFeatures(dict_features)
	# updateUser('ddgpsaqf',user_ft)
	filters = wit_extract_filters(dict_features)
	# print filters
	print getProjects(filters)
	print msg_features