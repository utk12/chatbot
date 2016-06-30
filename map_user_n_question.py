import json
from elasticsearch import Elasticsearch

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
	with open('Data/question_features_'+str(operation)+'_output.json') as json_data:
		json.dump(feature,json_data)

def update_weights(id,operation):
	user_feature = get_user_features(id)
	for key in user_feature:
		for sub_keys in user_feature[key]['children']:
			if int(user_feature[key]['foundValue']) > 0:
				if any(user_feature[key]['children'][sub_keys] >= 1):
					feature = load_question_feature_file(operation)
					feature[key]['weight'] = 0.0
					update_question_feature_file(operation,feature)
				else:
					feature = load_question_feature_file(operation)
					feature[key]['weight'] = 0.0
					update_question_feature_file(operation,feature)

if __name__ == '__main__':
	get_user_features('prirqlxu')
