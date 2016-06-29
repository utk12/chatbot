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
	fire = Firebase("https://friendlychat-1d26c.firebaseio.com/protectedResidential/9999/projects/")
	projects_all = fire.get()
	for i in projects_all:
		createProjectDataIndex(i, projects_all[i])
		createProjectFeaturesIndex(i])
		updateProjectFeatures(i)

def updateProjectFeatures(id):
	fire = Firebase("https://friendlychat-1d26c.firebaseio.com/protectedResidential/9999/projects/")
	projects_all = fire.get()
	price_range,size_range = price_size_range(projects_all)
	updated_features = all_features_mapping(getProjectFeaturesDoc(id), getProjectDataDoc(id), price_range, size_range)
	es.update(index = 'projects', doc_type = 'features', id = id, body = {"doc" : updated_features})

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
	es.update(index='projects',doc_type='features',id=project,body=body)
	

>>>>>>> fb7778bc402a88c4480f8f64b2e64900a710ea32
def updateProject(project):
	projectDict = getProjectDoc(project)
	for intent in projectDict:
		for category in projectDict[intent]:
			weightSum = 0.0
			total = 0.0
			for feature in projectDict[intent][category]['children']:
				found = float(projectDict[intent][category]['children'][feature]['foundValue'])
				weight = float(projectDict[intent][category]['children'][feature]['factorValue'])
				weightSum += weight*found
				total += weight

			projectDict[intent][category]['ratioScore'] = weightSum/total
	updateProjectJson(project, projectDict)

def getProjectVector(project, intent):
	projectDict = getProjectDoc(project)[intent]
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

<<<<<<< HEAD
=======
createProjectsDatabase()

>>>>>>> fb7778bc402a88c4480f8f64b2e64900a710ea32
# createProjectJSON(getProjectId())
# updateProject('ugzjugjc')
# print getProjectVector('ugzjugjc', 'buy')