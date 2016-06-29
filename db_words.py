import pandas as pd
from nltk.corpus import stopwords
from stringprocessing import *
import json

stop = stopwords.words('english')


def update_count_json(word_list):
	with open('Data/count.json', 'r') as f:
		count = json.loads(f.read())
	max_count = 0
	for i in count:
		max_count = max(max_count,count[i]) 
	for word in word_list:
		count[word] =  max_count
	with open('Data/count.json', 'w') as f:
		json.dump(count, f)


def questionCSVData():
	data = pd.read_csv('Data/data3.csv')
	rel_data = data.loc[data['Relevant'] == 'Yes']

	replies = list(rel_data['Bot_reply'])
	queries = list(rel_data['User_query'])

	replies += queries

	word_list = []
	for reply in replies:
		words = stringToWords(reply.lower())
		for word in words:	
			if word not in stop:
				word_list.append(word)
	return list(set(word_list))



def projectCSVData():
	data = pd.read_csv('Data/List of projects and developers Gurgaon.csv')
	word_list = []
	for row in data:
		for line in data[row]:
			words = stringToWords(line.lower())
			for word in words:	
				if word not in stop:
					word_list.append(word)
	return list(set(word_list))


def databaseWords():
	with open('Data/project_data.txt', 'r') as f:
		lines = f.readlines()

	word_list = []
	for line in lines:
		line = ''.join(map(lambda x: x.lower() if not x.isupper() else " "+x.lower(), line))
		for word in line.split():
			if word not in stop:
				word_list.append(word.lower())
	return list(set(word_list))

def specialWords():
	with open('Data/specialwords.txt', 'r') as f:
		lines = f.readlines()
	word_list = []
	for line in lines:
		line = ''.join(map(lambda x: x.lower() if not x.isupper() else " "+x.lower(), line))
		for word in line.split():
			if word not in stop:
				word_list.append(word.lower())
	return list(set(word_list))


def add_to_roofpik_data(word_list):
	with open('Data/roofpik_data.txt', 'a') as f:
		data = ""
		for word in word_list:
			data += word + '\n'
		f.write(data)

def removeDuplicate():
	with open('Data/roofpik_data.txt', 'r') as f:
		lines = f.readlines()

	lines = list(set(lines))		
	with open('Data/roofpik_data.txt', 'w') as f:
		f.writelines(lines)


def getRoofpikData():
	with open('Data/roofpik_data.txt', 'r') as f:
		lines = f.readlines()
	word_list = []
	for line in lines:
		word_list.append(line.replace('\n', ''))
	return list(set(word_list))


# print databaseWords()
# add_to_roofpik_data(databaseWords())
# add_to_roofpik_data(projectCSVData())
# add_to_roofpik_data(questionCSVData())
# print specialWords()
# add_to_roofpik_data(specialWords())
# removeDuplicate()

# update_count_json(getRoofpikData())