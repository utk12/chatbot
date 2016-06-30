from elasticsearch import Elasticsearch
from random import choice, randint
from string import ascii_lowercase
import json
import numpy as np
from firebase import Firebase
from project_feature_mapping import *

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

def genRandString(n):
	return (''.join(choice(ascii_lowercase) for i in range(n)))

def getProjectId():
	return genRandString(8)

def createProjectDataIndex(id, data):
	es.index(index='projects', doc_type='data', id=id, body=data)
	
def createProjectFeaturesIndex(id):
	with open('Data/project_features.json', 'r') as f:
		data = f.read()
	es.index(index='projects', doc_type='features', id=id, body=data)
	

def createProjectsDatabase():
	fire = Firebase("https://friendlychat-1d26c.firebaseio.com/protectedResidential/9999/projects/-KLLdC7joRUmOsT11Efp/")
	i = '-KLLdC7joRUmOsT11Efp'
	temp = fire.get()
	# projects_all = fire.get()
	# for i in projects_all:
	# createProjectDataIndex(i, projects_all[i])
	createProjectDataIndex(i, temp 	)
	createProjectFeaturesIndex(i)
	updateProjectFeatures(i)

def updateProjectFeatures(id):
	fire = Firebase("https://friendlychat-1d26c.firebaseio.com/protectedResidential/9999/projects/-KLLdC7joRUmOsT11Efp")
	temp = fire.get()
	# projects_all = fire.get()
	# print json.dumps(temp, indent = 4)
	price_range,size_range = price_size_range({"-KLLdC7joRUmOsT11Efp" : temp})
	# print price_range, size_range
	updated_features = all_features_mapping(getProjectDataDoc(id), getProjectFeaturesDoc(id), price_range, size_range)
	es.update(index = 'projects', doc_type = 'features', id = id, body = {"doc" : updated_features})
	# updateProject(id)


def getProjectFeaturesDoc(project):
	body = {
		"query" : {
			"match": {
				"_id" : project
			}
		}
	}
	return es.search(index='projects', doc_type='features', body = body)['hits']['hits'][0]['_source']


def getProjectDataDoc(project):
	body = {
		"query" : {
			"match": {
				"_id" : project
			}
		}
	}
	return es.search(index='projects', doc_type='data', body = body)['hits']['hits'][0]['_source']


def updateProjectJson(project, projectDict):
	body = {
		"doc" : projectDict
	}
	print projectDict
	es.update(index='projects',doc_type='features',id=project,body=body)
	

def updateProjectsRatios():
	project_list = es.search(index='projects', doc_type='features', body = {})['hits']['hits']
	for i in range(len(project_list)):
		p_id = project_list[i]['_id']
		projectDict = project_list[i]['_source']
		for category in projectDict:
			weightSum = 0.0
			total = 0.0
			for feature in projectDict[category]['children']:
				found = float(projectDict[category]['children'][feature]['foundValue'])
				weight = float(projectDict[category]['children'][feature]['factorValue'])
				weightSum += weight*found
				total += weight

			projectDict[category]['ratioScore'] = weightSum/total
		updateProjectJson(p_id, projectDict)

def getProjectVector(project, intent):
	projectDict = getProjectFeaturesDoc(project)[intent]
	vec = []
	for category in projectDict:
		vec.append(float(projectDict[category]['ratioScore']))
	vec = np.array(vec)
	mag = np.linalg.norm(vec)
	if mag > 0: 
		unit_vec = vec/mag
	else:
		unit_vec = vec
	return unit_vec


# createProjectsDatabase()
# updateProjectsRatios()
# createProjectJSON(getProjectId())
# updateProject('ugzjugjc')
# print getProjectVector('ugzjugjc', 'buy')