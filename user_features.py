from elasticsearch import Elasticsearch
from random import choice, randint
from string import ascii_lowercase
import json
import numpy as np
from update_question_features import convert_underscore_to_camelcase as toCamel

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

def genRandString(n):
	return (''.join(choice(ascii_lowercase) for i in range(n)))

def getUserId():
	return genRandString(8)

def createUserJSON(user):
	with open('Data/user_features.json', 'r') as f:
		data = json.loads(f.read())
	es.index(index='users', doc_type='features', id=user, body=data)

def getUserDoc(user):
	body = {
		"query" : {
			"match": {
				"_id" : user
			}
		}
	}
	return es.search(index='users', doc_type='features', body = body)['hits']['hits'][0]['_source']

def get_feature_dictionary():
	with open('Data/user_features.json', 'r') as f:
		data = json.loads(f.read())
	feature_dict = {}
	feature_dict = {}
	for category in data:
		category_new = ''.join(map(lambda x: x.lower() if not x.isupper() else "_"+x.lower(), category))
		feature_dict[category_new] = []
		for subcategory in data[category]['children']:
			if 'BHK' in subcategory:
				subcategory = subcategory.lower()
			else:
				subcategory = ''.join(map(lambda x: x.lower() if not x.isupper() else "_"+x.lower(), subcategory))
			feature_dict[category_new].append(subcategory)
	return feature_dict

def updateJson(user, userDict):
	body = {
		"doc" : userDict
	}
	es.update(index='users',doc_type='features',id=user,body=body)
	
def updateUser(user, features):
	userDict = getUserDoc(user)
	for i in features:
		i = toCamel(i)
		if i in userDict:
			userDict[i]['foundValue'] = 1
			nfeatures = len(userDict[i]['children'])
			userDict[i]['preferCount'] = nfeatures/2 + (nfeatures == 1)
			userDict[i]['factorValue'] += 0.5
		else :
			for child in userDict:
				if i in userDict[child]["children"]:
					temp = userDict[child]["children"][i] 
					userDict[child]["children"][i] = 1
					userDict[child]['foundValue'] = 1
					userDict[child]['preferCount'] += abs(temp-1)
					break
	updateJson(user,userDict)

def getUserVector(user):
	userDict = getUserDoc(user)
	vec = []
	for category in userDict:
		a = float(userDict[category]['foundValue'])
		b = float(userDict[category]['preferCount'])
		c = float(userDict[category]['factorValue'])
		vec.append(a*b*c)
	vec = np.array(vec)
	print vec
	mag = np.linalg.norm(vec)
	if mag > 0:	
		unit_vec = vec/mag
	else:
		unit_vec = vec
	return unit_vec

# print getUserVector('uyzpanbd',
# updateUser('uyzpanbd', ['security', 'amenities', '2BHK'])
# print getUserDoc('hndwkoiq')
# createUserJSON(getUserId())
# print get_feature_dictionary()
# feature_dict = get_feature_dictionary()
# features = get_features(user_query)