# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 16:08:57 2016

@author: utkarsh
"""
import json
from firebase import firebase
firebase = firebase.FirebaseApplication('https://friendlychat-1d26c.firebaseio.com', None)
data = firebase.get('/protectedResidential/',None)
print json.dumps(data,indent =4)