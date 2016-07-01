import pandas as pd
import os
pd.set_option('expand_frame_repr', False)
data = pd.read_csv('Data/List of projects and developers Gurgaon.csv')

from chatbot import remove_punct

def get_project_names():
	project_names = []
	for item in data['Project_Name']:
		item = item.lower()
		item = remove_punct(item)
		project_names.append(item)
	return project_names