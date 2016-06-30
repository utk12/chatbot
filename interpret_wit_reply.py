from user_features import get_feature_dictionary
import json
from wit_get_reply_api import get_all_entities_list_wit

def getFeatures(witReply):
	witReply = format_wit_reply(witReply)
	features = []
	features += (getRelativeFeatures(witReply))
	features += (getSecurityFeatures(witReply))
	for entity in witReply:
		for feature in witReply[entity]:
			f = extractFeatures(entity,feature)
			if f is not None:
				features.append(f)
	return features

def format_wit_reply(witReply):
	reply = {}
	for i in witReply:
		x = '_'.join(i.split())
		reply[x] = {}
		for j in witReply[i]:
			reply[x]['_'.join(str(j).split())] = witReply[i][j]
	return reply

def getRelativeFeatures(witReply):
	features = []
	if 'area' in witReply:
		if 'level' in witReply:
			levels = ['low', 'lower', 'high', 'greater', 'medium']
			for level in witReply['level']:
				if level in levels[:2]:
					features.append('area_low')
				elif level in levels[2:4]:
					features.append('area_high')
				elif level in levels[4:]:
					features.append('area_medium')
	return list(set(features))

def getSecurityFeatures(witReply):
	if 'security' not in witReply:
		return []

	features = []
	security = witReply['security']
	if 'security_place' in witReply:
		place = witReply['security_place']
		for i in place:
			for feature in security:
				features.append(feature+'_'+i)
	else:
		for feature in security:
			features.append(feature + '_' + 'tower')
			features.append(feature + '_' + 'maingate')

	return list(set(features))

def extractFeatures(entity, feature):
	feature_dict = get_feature_dictionary()
	if entity == 'feature':
		if feature in feature_dict:
			return feature

	x = ['project_type', 'configurations', 'specifications', 'amenities', 'accommodation', 'possession']
	if entity in x:
		if entity == 'configurations':
			entity = 'specifications'
		if feature in feature_dict[entity]:
			return feature

# print get_entities_list_wit()
# getFeatures({u'security': {u'cctv': True}, u'security_place': {u'tower': True}, u'project_type': {u'row house': True}, u'sentiment': {u'positive': True}}, 'buy')


# print get_feature_dictionary()
# print json.dumps(get_feature_dictionary()['buy'], indent = 4)