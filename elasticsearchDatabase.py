from elasticsearch import Elasticsearch
from yo import *

es = Elasticsearch([{'host':'localhost','port':9200}])

def createLocationsDatabase(locs):
	for i,j in locs:
		es.index(index = 'roofpik', doc_type = 'locations', id = i, body = {"name" : j})

def createZonesDatabase(zones):
	for i,j in zones:
		es.index(index = 'roofpik', doc_type = 'zones', id = i, body = {"name" : j})

def createCitiesDatabase(cities):
	for i,j in cities:
		es.index(index = 'roofpik', doc_type = 'cities', id = i, body = {"name" : j})

def createBuildersDatabase(builders):
	for i,j in builders:
		es.index(index = 'roofpik', doc_type = 'builders', id = i, body = {"name" : j})

def getLocationId(loc):
	body = {
		"query" : {
			"match_phrase": {
				"name" : loc
			}
		}
	}	
	return es.search(index = 'roofpik', doc_type = 'locations', body = body)

def getZoneId(zone):
	body = {
		"query" : {
			"match_phrase": {
				"name" : zone
			}
		}
	}	
	return es.search(index = 'roofpik', doc_type = 'zones', body = body)

def getCityId(city):
	body = {
		"query" : {
			"match_phrase": {
				"name" : city
			}
		}
	}	
	return es.search(index = 'roofpik', doc_type = 'cities', body = body)

def getBuilderId(builder):
	body = {
		"query" : {
			"match_phrase": {
				"name" : builder
			}
		}
	}	
	return es.search(index = 'roofpik', doc_type = 'builders', body = body)

def getProjectId(project):
	body = {
		"query" : {
			"match_phrase": {
				"projectDetails.projectName" : project
			}
		}
	}	
	return es.search(index = 'projects', doc_type = 'data', body = body)

if __name__ == '__main__':
	createLocationsDatabase(get_tuple_location())
	createZonesDatabase(get_tuple_zone())
	createBuildersDatabase(get_tuple_builders())
	createCitiesDatabase(get_tuple_city())
