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
from chatbot import sleep
import datetime

def chatbot(message,user):
	# message = 'I want a  house in which we should have tennis and servant room with area less than 1200 sq.ft.'
	t1 = datetime.datetime.now()
	message =  main(message) # spell correct
	t2 = datetime.datetime.now()
	print t2-t1
	# print message
	# message = 'I want a house in which we should have tennis and servant room with price greater than 1200 rs'
	t1 = datetime.datetime.now()
	entities = get_entities_json_wit(message) #this is json object of entities from wit.
	t2 = datetime.datetime.now()
	print t2-t1
	# msg_features = get_entities_from_msg_Wit(message)
	# print msg_features
	t1 = datetime.datetime.now()
	dict_features = interpret_wit_output(entities) #structure derived from wit reply.
	t2 = datetime.datetime.now()
	print t2-t1
	# print dict_features
	# print json.dumps(entities,indent = 4)
	# print dict_features
	t1 = datetime.datetime.now()
	user_ft =  getFeatures(dict_features) # extract user features to be used from wit reply
	t2 = datetime.datetime.now()
	print t2-t1
	t1 = datetime.datetime.now()
	updateUser(user,user_ft) #updated user features in elastic search
	t2 = datetime.datetime.now()
	print t2-t1
	t1 = datetime.datetime.now()
	filters = wit_extract_filters(dict_features) #extract filters from wit reply
	t2 = datetime.datetime.now()
	print t2-t1
	# print filters
	t1 = datetime.datetime.now()
	project_list = getProjects(filters, user) #
	t2 = datetime.datetime.now()
	print t2-t1
	print project_list
	# project_list_sorted = sortProjects(project_list, user)
	# print project_list_sorted
	# print msg_features
	t1 = datetime.datetime.now()
	print get_suggestions(user, 'buy')
	t2 = datetime.datetime.now()
	print t2-t1

if __name__ == '__main__':
    print('Hey there ! Enter a query to chat.\n')
    while(True):
        inp = raw_input()
        if inp == 'Bye' or inp == 'bye':
            print 'Have a good day.',
            sleep(3)
            break
        chatbot(inp,'prirqlxu')