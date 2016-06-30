from interpret_wit_reply import format_wit_reply
import json


def getFiltersJson():
	with open('Data/filters.json', 'r') as f:
		data = json.loads(f.read())
	result = {}
	for cat in data:
		cat1 = 	''.join(map(lambda x: x.lower() if not x.isupper() else "_"+x.lower(), cat))
		result[cat1] = {}
		for i in data[cat]:
			subcat = ''.join(map(lambda x: x.lower() if not x.isupper() else "_"+x.lower(), i))
			if isinstance(data[cat][i], dict):
				result[cat1][subcat] = {}
				for j in data[cat][i]:
					key = ''.join(map(lambda x: x.lower() if not x.isupper() else "_"+x.lower(), j))
					result[cat1][subcat][key] = ''
			else:
				result[cat1][subcat] = ''
	# print json.dumps(result, indent=4)
	return result

filters_data = getFiltersJson()

def wit_extract_filters(witReply):
	witReply = format_wit_reply(witReply)
	filters = {}
	filters['project_details'] = getProjectDetails(witReply)
	filters['sports_activities'], filters['club_house'] = getAmenitiesFilters(witReply)
	filters['specifications'] = getSpecifications(witReply)
	filters['other'], filters['configurations'] = getConfigurations(witReply)
	filters['security'] = getSecurityFilters(witReply)
	return filters

def getProjectDetails(witReply):
	details = {}
	list1 = ['project_name', 'builder']
	for i in list1:
		if i in witReply:
			details[i] = {}
			for j in witReply[i]: 
				details[i][j] = True

	details['address'] = {}
	if 'loc_city' in witReply:
		for i in witReply['loc_city']: 
			details['address']['city'] = i
			break

	if 'address_zone' in witReply:
		details['address']['zone'] = {}
		for i in witReply['address_zone']:
			details['address']['zone'][i] = True

	if 'specifications' in witReply:
		if 'parking' in witReply['specifications']:
			details['car_parking'] = True
		if 'vastu' in witReply['specifications']:
			details['vastu_compliant'] = True

	return details




def getSecurityFilters(witReply):
	filters = {}
	if 'security' in witReply:
		if 'security_place' in witReply:
			filters['place_flag'] = True
			for i in witReply['security_place']:
				filters[i] = {}
				for j in witReply['security']:
					if j in filters_data['security'][i]:
						filters[i][j] = True
		else:
			filters['place_flag'] = False
			for i in witReply['security']:
				if i in filters_data['security']['tower']:
					filters['tower'][i] = True
				elif i in filters_data['security']['main_gate']:
					filters['main_gate'][i] = True
	return filters


def getSpecifications(witReply):
	filters = {}
	if 'specifications' in witReply:
		for i in witReply['specifications']:
			if i == 'modular_kitchen':
				i = 'kitchen_modular'
			if i in filters_data['specifications']:
				filters[i] = True
	return filters



def getAmenitiesFilters(witReply):
	sports = {}
	club = {}
	if 'amenities' in witReply:
		for i in witReply['amenities']:
			if i in filters_data['sports_activities']:
				sports[i] = True
			elif i in filters_data['club_house']:
				club[i] = True
	return sports, club



def getConfigurations(witReply):
	others = {}
	configurations = {}
	if 'configurations' in witReply:
		for i in witReply['configurations']:
			if i in filters_data['other']:
				others['i'] = True
			elif i in filters_data['configurations']:
				configurations[i] = True
	if 'project_type' in witReply:
		configurations['property_type'] = {}
		for i in witReply['project_type']:
			configurations['property_type'][i] = True
	if 'accommodation' in witReply:
		configurations['type'] = {}
		for i in witReply['accommodation']:
			configurations['type'][i] = True
	if 'area' in witReply:
		for i in witReply['area']:
			configurations['area'] = i
			break
		if 'level' in witReply:
			for i in witReply['level']:
				if i in ['high', 'greater']:
					i = 'high'
				elif i in['low', 'lower']:
					i = 'low'
				else:
					i = 'medium'
				configurations['area_level'] = i
				break
		else:
				configurations['area_level'] = 'medium'

	if 'amount_of_money' in witReply:
		for i in witReply['amount_of_money']:
			configurations['price'] = i
			break
		if 'level' in witReply:
			for i in witReply['level']:
				if i in ['high', 'greater']:
					i = 'high'
				elif i in['low', 'lower']:
					i = 'low'
				else:
					i = 'medium'
				configurations['price_level'] = i
				break
		else:
			configurations['price_level'] = 'medium'

	return others, configurations





# wit_extract_filters({u'security': {u'cctv': True}, u'security_place': {u'tower': True}, u'project_type': {u'row house': True}, u'sentiment': {u'positive': True}, 'loc_city' : {'gurgaon':True}, 'address_zone' : {'sohna road':True}, 'amenities' : {'football':True}})
