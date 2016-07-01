import json
from elasticsearch import Elasticsearch
import numpy as np

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

def get_user_features(id):
	user_feature = es.get(index='users',doc_type='features',id=id)
	user_feature = user_feature['_source']
	return user_feature
	# print json.dumps(user_feature,indent = 4)

def load_question_feature_file(operation):
	with open('Data/question_features_'+str(operation)+'_output.json') as json_data:
		feature = json.loads(json_data.read())
	return feature

def update_question_feature_file(operation,feature):
	try:
		with open('Data/question_features_'+str(operation)+'_output.json', 'w') as json_data:
			json.dump(feature,json_data, indent=4)
			return "hello"
	except (OSError, IOError) as e:
		return str(e)

def normalize_weights(weight_list,input_json,operation):
	vec = []
	for i,j in weight_list:
		vec.append(i)
	vec = np.array(vec)
	mag = np.linalg.norm(vec)
	if mag > 0: 
		unit_vec = vec/mag
	else:
		unit_vec = vec
	# print input_json
	for i in range(len(weight_list)):
		feature = weight_list[i][1]
		input_json[feature]['weight'] = unit_vec[i]
	update_question_feature_file(operation,input_json)

def update_weights(id,operation):
	user_feature = get_user_features(id)
	for key in user_feature:
		if int(user_feature[key]['foundValue']) > 0:
			feature = load_question_feature_file(operation)
			weight_list = get_keys_weight(feature)
			if any(value >= 1 for key,value in user_feature[key]['children'].iteritems()):
				feature[key]['weight'] = min(weight_list)[0]/2
				update_question_feature_file(operation,feature)
			else:
				feature[key]['weight'] = (max(weight_list)[0] + 1)/2
				update_question_feature_file(operation,feature)
			weight_list = get_keys_weight(feature)
			normalize_weights(weight_list,feature,operation)

def top_three_questions(feature):
	keys_list = get_keys_weight(feature)
	keys_list.sort(reverse = True)
	return [j for i,j in keys_list[:3]]

def get_keys_weight(feature):
	list1 = []
	for key in feature:
		list1.append([feature[key]['weight'],key])
	return list1

def get_suggestions(id,operation):
	feature = load_question_feature_file(operation)
	update_weights(id,operation)
	# return feature
	top_features = top_three_questions(feature)
	questions_list = [feature[key]['bot_question'] for key in top_features]
	return questions_list

# if __name__ == '__main__':
	# get_user_features('prirqlxu')
	# update_weights('prirqlxu','buy')
	# top_three_questions(load_question_feature_file('buy'))
	# print get_suggestions(load_question_feature_file('buy'))
