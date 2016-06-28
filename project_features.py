from elasticsearch import Elasticsearch
from random import choice, randint
from string import ascii_lowercase
import json
import numpy as np

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
def genRandString(n):
    return (''.join(choice(ascii_lowercase) for i in range(n)))

def getProjectId():
    return genRandString(8)

def createProjectJSON(project):
    with open('Data/project_features.json', 'r') as f:
        data = f.read()
    es.index(index='projects', doc_type='features', id=project, body=data)

def getProjectDoc(project):
    body = {
        "query" : {
            "match": {
                "_id" : project
            }
        }
    }
    return es.search(index='projects', doc_type='features', body = body)['hits']['hits'][0]['_source']



def updateProjectJson(project, projectDict):
    body = {
        "doc" : projectDict
    }
    es.update(index='projects',doc_type='features',id=project,body=body)
    

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


# createProjectJSON(getProjectId())
# updateProject('ugzjugjc')
# print getProjectVector('ugzjugjc', 'buy')