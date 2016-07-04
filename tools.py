import json
def convert_underscore_to_camelcase(text):
	components = text.split('_')
	return components[0] + "".join(x.title() for x in components[1:])

def convert_camelcase_to_underscore(str):
	return ''.join(map(lambda x: x.lower() if not x.isupper() else "_"+x.lower(),str))

def to_underscore(filters):
	result = {}
	for i in filters:
		i_new = convert_camelcase_to_underscore(i)
		result[i_new] = {}
		for j in filters[i]:
			j_new = convert_camelcase_to_underscore(j)
			if i == "projectDetails":
				if j == 'address' or j == 'projectType':
					result[i_new][j_new	] = {}
					for k in filters[i][j]:
						k_new = convert_camelcase_to_underscore(k)
						result[i_new][j_new][k_new] = filters[i][j][k]
				else:
					result[i_new][j_new] = filters[i][j]
			elif i == 'security':
				result[i_new][j_new	] = {}
				for k in filters[i][j]:
					k_new = convert_camelcase_to_underscore(k)
					result[i_new][j_new][k_new] = filters[i][j][k]
			else:
				result[i_new][j_new] = filters[i][j]
	return result

def to_camelcase(filters):
	result = {}
	for i in filters:
		i_new = convert_underscore_to_camelcase(i)
		result[i_new] = {}
		for j in filters[i]:
			j_new = convert_underscore_to_camelcase(j)
			if i == "project_details":
				if j == 'address' or j == 'project_type':
					result[i_new][j_new	] = {}
					for k in filters[i][j]:
						k_new = convert_underscore_to_camelcase(k)
						result[i_new][j_new][k_new] = filters[i][j][k]
				else:
					result[i_new][j_new] = filters[i][j]
			elif i == 'security':
				result[i_new][j_new	] = {}
				for k in filters[i][j]:
					k_new = convert_underscore_to_camelcase(k)
					result[i_new][j_new][k_new] = filters[i][j][k]
			else:
				result[i_new][j_new] = filters[i][j]
	return result

with open('Data/filters.json') as json_file:
	filters = json.loads(json_file.read())
filters = to_underscore(filters)
print json.dumps(to_camelcase(filters),indent = 4)
