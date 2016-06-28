import json
from sentence_corrector import main
from wit_get_reply_api import *
from user_features import *
from interpret_wit_reply import *
from getFilters import *
from applyFilters import *

def sleep(n):
    for i in range(n):
        time.sleep(1)
        print '.',
        sys.stdout.flush()
    print('bye!!')

#==============================================================================
# if __name__ == '__main__':
#     print('Hey there ! Enter a query to chat.\n')
#     while(True):
#         inp = raw_input()
#         if inp == 'Bye' or inp == 'bye':
#             print 'Have a good day.',
#             sleep(3)
#             break
#         print(get_reply(inp))
#==============================================================================

if __name__ == '__main__':
	message = 'I want a row-house in golf corse road which should have cricket and football'
	message =  main(message)
	entities = get_entities_json_wit(message) #this is json object of entities from wit.
	dict_features = interpret_wit_output(entities)
	# print json.dumps(entities,indent = 4)
	# print dict_features
	# user_ft =  getFeatures(dict_features)
	# updateUser('ddgpsaqf',user_ft)
	filters = wit_extract_filters(dict_features)
	print filters
	print getProjects(filters)
