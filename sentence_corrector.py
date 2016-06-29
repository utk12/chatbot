import json
from english_corrector import EnglishCorrector
from chatbot import *

def main(str1):
	str1 = str1.lower()
	ec = EnglishCorrector()
	if(len(str1)>0):
		res = ec.correct(str1)
	return res

def getInput():
	print("Enter sentence to correct (Give blank input to exit):")
	sentence = raw_input()
	return sentence.lower()

def show(text):
	print(json.dumps(text,indent=2))
	