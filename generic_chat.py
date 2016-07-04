from flask import Blueprint, jsonify
from flask_restful import reqparse
import json
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

from sentence_corrector import spell_correct
from generic_replies import get_reply

generic_chat_blueprint = Blueprint('generic_chat_blueprint', __name__)

@generic_chat_blueprint.route('/generic_chat')
def post():
	parser = reqparse.RequestParser()
	parser.add_argument('msg', type=str)
	parser.add_argument('operation', type=str)

	args = parser.parse_args()
	message = args['msg']
	operation = args['operation']
	message =  spell_correct(message)
	reply = get_reply(message)
	return  jsonify({"reply" :  reply})
