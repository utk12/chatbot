from wit_get_reply_api import *

def get_message_conv():
	results = []
	with open('') as text_file:
		results.append(line.split('\n'))
	for sent in results:
		get_entities_from_msg_Wit(sent)