import requests,json
from get_project_names import get_project_names
#get_message
#Use different session ids for different users

def get_message_format_wit(str):
	str.replace(' ','%20')
	return str

def get_say_action_wit(message):
	message = get_message_format_wit(message)
	headers = {'Authorization':'Bearer QZBAVFA3VWR3UBH4PDUCGWELMGIE2T4O'}
	url = 'https://api.wit.ai/converse?v=20160624&session_id=8&q='+str(message)
	r = requests.post(url=url,headers = headers)
	obj = json.loads(r.text)
	while(obj['type'] != 'msg'):
		r = requests.post('https://api.wit.ai/converse?v=20160624&session_id=8',data={},
			headers = headers)
		obj = json.loads(r.text)
	return obj['msg']

def get_output_wit(message):
	headers = {'Authorization':'Bearer QZBAVFA3VWR3UBH4PDUCGWELMGIE2T4O'}
	message = get_message_format_wit(message)
	url = 'https://api.wit.ai/message?v=20160624&session_id=8&q='+str(message)
	r = requests.post(url=url,headers = headers)
	obj = json.loads(r.text)
	return obj

def get_all_entities_list_wit():
	headers = {'Authorization':'Bearer QZBAVFA3VWR3UBH4PDUCGWELMGIE2T4O'}
	url = 'https://api.wit.ai/entities'
	r = requests.get(url=url,headers = headers)
	obj = r.text
	return obj

def get_entities_from_msg_Wit(message):
	wit_reply = get_output_wit(message)
	list1 = []
	for item in wit_reply['entities']:
		list1.append(item)
	return list1

def get_entities_json_wit(message):
	json_object = get_output_wit(message)
	entities = {}
	for key,value in json_object.iteritems():
		if key == 'entities':
			entities = json_object[key]
	return entities

def create_new_entity_wit(entity,values):
	headers = {'Authorization':'Bearer QZBAVFA3VWR3UBH4PDUCGWELMGIE2T4O'}
	url	= 'https://api.wit.ai/entities?v=20160624'
	data = {}
	data['id'] = entity
	data['values'] = []
	for item in values:
		dict1 = {}
		dict1['value'] = item
		data['values'].append(dict1)
	data = json.dumps(data)
	r=requests.post(url=url,headers = headers,data = data)
	print r.text

def delete_entity(entity):
	headers = {'Authorization':'Bearer QZBAVFA3VWR3UBH4PDUCGWELMGIE2T4O'}
	r = requests.delete('https://api.wit.ai/entities/'+str(entity)+'?v=20160624',
		headers = headers)

def add_new_value_entity(entity,value):
	headers = {'Authorization':'Bearer QZBAVFA3VWR3UBH4PDUCGWELMGIE2T4O'}
	url = 'https://api.wit.ai/entities/'+str(entity)+'/values?v=20160624'
	data = {}
	# data['values'] = []
	# for item in values:
	# 	dict1 = {}
	# 	dict1['value'] = item
	# 	data['values'].append(dict1)
	# data = json.dumps(data)
	data['value'] = value
	data = json.dumps(data)
	r = requests.post(url=url,headers=headers,data=data)
	print r.text

def interpret_wit_output(json_object):
	# list1 = []
	dict1 = {}
	for key in json_object:
		dict1[key] = {}
		for i in range(len(json_object[key])):
			dict1[key][json_object[key][i]['value']] = True
	return dict1

if __name__ == '__main__':
	# entity = 'trial'
	# values = ['1','2']
	# create_new_entity_wit(entity,values)
	# delete_entity('trial')
	# value = '3'
	# add_new_value_entity(entity,value)
	# entity = 'project_name'
	# values = get_project_names()
	# create_new_entity_wit(entity,values)
	message = 'I want a row-house with cricket facilities nearby.'
	print get_entities_from_msg_Wit(message)
