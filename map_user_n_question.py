import json
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

def get_user_features(id):
	user_features = es.get(index='users',doc_type='features',id=id)
	print json.dumps(user_features,indent = 4)

if __name__ == '__main__':
	get_user_features('prirqlxu')