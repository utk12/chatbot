# from getFilters import wit_extract_filters
from elasticsearch import Elasticsearch
import json
from update_question_features import convert_underscore_to_camelcase as toCamel

es = Elasticsearch([{'host':'localhost','port':9200}])

def getProjects(filters_dict):
	body = prepareBody(filters_dict)
	project_list = es_search(body)
	project_list = applyUnitsFilter(project_list, filters_dict)
	result = []
	for i in xrange(len(project_list)):
		result.append(project_list[i]['_id'])
	return result


def applyUnitsFilter(project_list, filters_dict):
	result = []
	if 'specifications' in filters_dict:
		specs = [i for i in filters_dict['specifications']]
	if 'configurations' in filters_dict:
		configs = [i for i in filters_dict['configurations']]
	for i in range(len(project_list)):
		for unit in project_list[i]['_source']['units']:
			flag = 1
			for spec in specs:
				if not project_list[i]['_source']['units'][unit]['specifications'][toCamel(spec)]:
					flag = 0
					break
			if flag == 1:
				for config in configs:
					if config == 'property_type':
						x = [toCamel(j) for j in filters_dict['configurations'][config]]
						if project_list[i]['_source']['units'][unit]['configurations'][toCamel(config)] not in x:
							flag = 0
							break
					elif config == 'type':
						x = [toCamel(j) for j in filters_dict['configurations'][config]]
						if ''.join(project_list[i]['_source']['units'][unit]['configurations'][toCamel(config)].split()).lower() not in x:
							flag = 0
							break
					elif config == 'price':
						price = project_list[i]['_source']['units'][unit]['configurations'][toCamel(config)]
						price_level = filters_dict['configurations']['price_level']
						price_supposed = filters_dict['configurations']['price']
						if price_level == 'high':
							if price < price_supposed:
								flag = 0
								break
						if price_level == 'low':
							if price > price_supposed:
								flag = 0
								break
					elif config == 'area':
						area = project_list[i]['_source']['units'][unit]['configurations']['superArea']
						area_level = filters_dict['configurations']['area_level']
						area_supposed = filters_dict['configurations']['area']
						print area
						print area_supposed
						print area_level
						if area_level == 'high':
							if area < area_supposed:
								flag = 0
								break
						elif area_level == 'low':
							if area > area_supposed:
								flag = 0
								break
					elif config == 'store_room' or config == 'servant_room':
						if not project_list[i]['_source']['units'][unit]['configurations'][toCamel(config)]:
							flag = 0
							break
			if flag == 1:
				result.append(project_list[i])
				break
	return result



def es_search(body):
	return es.search(index = 'projects', doc_type = 'data', body = body)['hits']['hits']


def prepareBody(filters_dict):
	fliterMust = []
	club = {"bool" : {"should" : []	}}
	for i in filters_dict['club_house']:
		i = toCamel(i)
		club['bool']['should'].append({"term":{'clubHouse.'+i : True}})

	sports = {"bool" : {"should" : [] }}
	for i in filters_dict['sports_activities']:
		i = toCamel(i)
		sports['bool']['should'].append({"term":{'sportsActivities.'+i : True}})

	other = {"bool" : {"must" : [] }}
	for i in filters_dict['other']:
		i = toCamel(i)
		other['bool']['must'].append({"term":{'other.'+i : True}})

	sec = {
		"bool" : {
			"should" : [],
			"must" : []	
		}
	}
	security = filters_dict['security']
	if len(security) > 0:
		if security['place_flag']:
			for i in security:
					if i != 'place_flag':
						for j in security[i]:
							i = toCamel(i)
							j = toCamel(j)
							sec['bool']['must'].append({"term":{"security."+i+"."+j : True}})
		else:
			for i in security:
				if i != 'place_flag':
					for j in security[i]:
						i = toCamel(i)
						j = toCamel(j)
						sec['bool']['should'].append({"term":{"security."+i+"."+j : True}})

	details = {"bool" : {"must" : [] }}
	
	for i in filters_dict['project_details']:
		if i == 'project_name' or i == 'builder':
			x = []
			for j in filters_dict['project_details'][i]:
				i = toCamel(i)
				j = toCamel(j)
				x.append({"match_phrase":{'projectDetails.'+i : j}})
			details['bool']['must'].append({'bool' : {'should':x}})

		elif i == 'project_type':
			x = []
			for j in filters_dict['project_details'][i]:
				i = toCamel(i)
				j = toCamel(j)
				x.append({"term":{'projectDetails.'+i+'.'+j : True}})
			details['bool']['must'].append({'bool' : {'should':x}})

		elif i == 'car_parking' or i == 'vastu_compliant':
			i = toCamel(i)
			details['bool']['must'].append({"term":{'projectDetails.'+i : True}})

		elif i == 'address':
			x = []
			for j in filters_dict['project_details'][i]:
				if j == 'city':
					x.append({"match_phrase":{"projectDetails."+toCamel(i)+".cityName" : filters_dict['project_details'][i][j]}})
				elif j == 'zone':
					y = {'bool':{'should' : []}}
					for k in filters_dict['project_details'][i][j]:
						y['bool']['should'].append({"match_phrase":{"projectDetails."+toCamel(i)+".zoneName" : k}})
					x.append(y)
				elif j == 'location':
					y = {'bool':{'should' : []}}
					for k in filters_dict['project_details'][i][j]:
						
						y['bool']['should'].append({"query_string":{"fields" : ["projectDetails."+toCamel(i)+".locations.*.locationName"], "query" : "\""+k+"\""}})
					x.append(y)
			details['bool']['must'].append({'bool' : {'must':x}})


	# specs = {"bool" : {"must" : [] }}
	# for i in filters_dict['specifications']:
	fliterMust.append(club)
	fliterMust.append(sports)
	fliterMust.append(sec)
	fliterMust.append(details)
	fliterMust.append(other)


	body = {
		"query": {
			"filtered" : {
				"query" : {
					"match_all" : {}
				},
				"filter" : [
					{
						"bool" : {
							"must" : fliterMust
						}
					}
				]
			}
		}
	}

	return body


