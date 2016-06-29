# import re
import json
import math
import numpy as np
from stringprocessing import *

class EnglishCorrector():

	def __init__(self,clusters_to_check=5):
		self.n_clusters = 1000
		self.clusters_to_check = clusters_to_check
		cluster_data_file = "Data/clusters.json"		
		count_data_file = "Data/count.json"
		with open(cluster_data_file, 'r') as f:
			self.clusters = json.load(f)
		with open(count_data_file, 'r') as f:
			self.word_counts = json.load(f)
		self.cluster_centers = []
		for i in range(self.n_clusters):
			self.cluster_centers.append(self.clusters[str(i)]["center"])

	def correct(self,sentence):
		ans = ''
		word_list = stringToWords(sentence,True)
		for typed_word in word_list:
			typed_word = typed_word.lower()
			word_letter_freq = getDistribution(typed_word)
			center_list = []
			for i in range(self.n_clusters):
				obj = {}
				obj["cluster_label"] = i
				obj["center_coords"] = self.cluster_centers[i]
				obj["vector_dist"] = np.linalg.norm(word_letter_freq-obj["center_coords"])
				center_list.append(obj)
			center_list.sort(key=lambda x: x['vector_dist'], reverse=False)
			# for item in center_list:
			# 	print(item['vector_dist'])
			words_to_check = []
			for i in range(self.clusters_to_check):
				cluster_label = center_list[i]["cluster_label"]
				for node in self.clusters[str(cluster_label)]["points"]:
					words_to_check.append(node["word"])
			# ans[typed_word] = getBestMatch(typed_word,words_to_check,self.word_counts)
			temp = getBestMatch(typed_word,words_to_check,self.word_counts)
			typed_word_suggestions = []
			for item in temp:
				typed_word_suggestions.append(item["word"])
			ans += typed_word_suggestions[0] + ' '
		return ans

def getBestMatch(typed_word,words_to_check,word_counts):
	result_len = 20
	match_threshold = 0
	result = []
	for lookup_word in words_to_check:
		word_score,scores = getWordRelevanceScore(typed_word,lookup_word,word_counts)
		if word_score>match_threshold:
			result.append({ 'word':lookup_word , 'score':word_score })
		if len(result)>2*result_len:
			result.sort(key=lambda x: x['score'], reverse=True)
			result = result[:result_len]
			match_threshold = result[result_len-1]["score"]
	result.sort(key=lambda x: x['score'], reverse=True)
	result = result[:result_len]
	for item in result:
		if item["word"] in word_counts:
			item_freq = word_counts[item["word"]]
			item["score"] += math.log(item_freq+1,10)
	result.sort(key=lambda x: x['score'], reverse=True)
	result = result[:result_len]
	return result


def getWordRelevanceScore(typed_word,lookup_word,word_counts):
	"""
	score:
		0: constant
		1: frequency
		2: word distance score
		3: longest common prefix
		4: longest common suffix
	"""
	scores = np.zeros(5)
	score_factors = np.array([ 1.0 , 0.1 , 4.0 , 1.0 , 0.75 ])
	word_score = 0
	typed_word_len = len(typed_word)
	lookup_word_len = len(lookup_word)

	if typed_word_len>0 and lookup_word_len>0:
		if lookup_word in word_counts:
			# print(lookup_word+" : "+str(word_counts[lookup_word]))
			scores[1] = math.log(word_counts[lookup_word]+1,10)
		scores[2] = dl_score_nuetral(typed_word,lookup_word)
		temp = lc_prefix(typed_word,lookup_word)
		if temp>1:
			scores[3] = scores[2]*math.log(temp+1,2)
		temp = lc_suffix(typed_word,lookup_word)
		if temp>1:
			scores[4] = scores[2]*math.log(temp+1,2)

	word_score = score_factors.transpose().dot(scores)
	return word_score,scores.tolist()


def getDistribution(word):
	word_letter_freq = np.zeros(26)
	for c in word:
		if c.isalpha():
			word_letter_freq[ord(c)-ord('a')] += 1
	return word_letter_freq


def show(text):
	print(json.dumps(text,indent=2))