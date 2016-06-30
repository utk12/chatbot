from wit_get_reply_api import *
import json

if __name__ == '__main__':
	# get_message_conv()
	conversations = []	
	with open('Data/conversations.txt') as text_file:
		text_file = text_file.read()
		conversations += text_file.split('\n\n')
	dict1 = {}
	i = 0
	for item in conversations:
		i += 1
		dict1[i]=item.split('\n')
	print json.dumps(dict1,indent = 4)
