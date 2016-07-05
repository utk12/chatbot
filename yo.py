import json
from firebase import Firebase

def build_firebase_connection(item):
	firebase = Firebase('https://roofpik-948d0.firebaseio.com/'+str(item))
	data = firebase.get()
	return data

def get_tuple_location():
	# item = location,zone
	data = build_firebase_connection('location')
	# print json.dumps(data,indent = 4)
	tuples = []
	for city_id in data:
		for loc_id in data[city_id]:
			tuples.append((loc_id,data[city_id][loc_id]['locationName']))
	return tuples

def get_tuple_zone():
	# item = location,zone
	data = build_firebase_connection('zone')
	# print json.dumps(data,indent = 4)
	tuples = []
	for city_id in data:
		for loc_id in data[city_id]:
			tuples.append((loc_id,data[city_id][loc_id]['zoneName']))
	return tuples

def get_tuple_builders():
	# item = location,zone
	data = build_firebase_connection('builders')
	# print json.dumps(data,indent = 4)
	tuples = []
	for builder_id in data:
		tuples.append((builder_id,data[builder_id]['name']))
	return tuples

def get_tuple_city():
	# item = location,zone
	data = build_firebase_connection('city')
	# print json.dumps(data,indent = 4)
	tuples = []
	for builder_id in data:
		tuples.append((builder_id,data[builder_id]['cityName']))
	return tuples

if __name__ == '__main__':
	print json.dumps(get_tuple_builders(),indent = 4)
	print json.dumps(get_tuple_city(),indent = 4)
	print json.dumps(get_tuple_location(),indent = 4)
	print json.dumps(get_tuple_zone(),indent = 4)	