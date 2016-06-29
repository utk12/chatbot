from wit_get_reply_api import *

def get_message_conv():
	results = []
	entities_list = []
	with open('') as text_file:
		results.append(line.split('\n'))
	for sent in results:
		entities_list.append(get_entities_from_msg_Wit(sent))
	print entities_list

if __name__ == '__main__':
	get_message_conv()