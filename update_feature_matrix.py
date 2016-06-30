from collections import Counter
import pandas as pd 
from featureOrder import default_order_dict

def create_new_chat_entry(wit_message,response,default_order,max_number):
    feature_order = {}
    wit_feature_order = {}
    response_mat = {}
    for n,key in enumerate(wit_message):
        print key,n
        if key in default_order:
            wit_feature_order[key] = default_order[key]
            response_mat[key] = response[n] 
    while wit_feature_order != {}:
        wit_key  = min(wit_feature_order,key=wit_feature_order.get)
        if feature_order == {}:
            feature_order[wit_key] = max_number + 1
        else:
            feature_order[wit_key] = max(feature_order.values())+1
            
        del wit_feature_order[wit_key]
    return feature_order,response_mat


def add_to_csv_file(message,response,chatID):
    q_csv_file = 'Q_order_CSV2.csv'
    a_csv_file = 'answers_CSV2.csv'
    
    q_data = pd.read_csv(q_csv_file,header=0,index_col=0)
    a_data = pd.read_csv(a_csv_file,header = 0,index_col=0)
    entry_string = 'chat'+str(chatID)
    default_order = default_order_dict(q_data)
    if entry_string in q_data.index:
        max_number = max(q_data.ix[entry_string])
    else:
        max_number = 0
    order_dict,response_dict = create_new_chat_entry(message,response,default_order,max_number)
    for feature in q_data.columns:
        if entry_string in q_data.index:
            if feature in order_dict:
                q_data[feature][entry_string] = order_dict[feature]
                a_data[feature][entry_string] = response_dict[feature]
        else:
            q_data.loc[entry_string] = [0]*10
            a_data.loc[entry_string] = [-1]*10
            if entry_string in order_dict:
                q_data[feature][entry_string] = order_dict[feature]
                a_data[feature][entry_string] = response_dict[feature]
    q_data.to_csv(q_csv_file)
    a_data.to_csv(a_csv_file)
    

def convert_space_to_underscore(str):
	return ''.join(map(lambda x:x.lower() if x != ' ' else "_",str))

def convert_underscore_to_camelcase(text):
	components = text.split('_')
	return components[0] + "".join(x.title() for x in components[1:])

def update_question_matrix(message,chatID):
    csv_file = 'Q_order_CSV2.csv'
    default_order = default_order_dict(csv_file)

    
    

if __name__ == '__main__':
    default_order = {'possession': 1, 'rating': 8, 'projectType': 2, 'specifications': 7, 'price': 4, 'amenities': 5, 'security': 9, 'size': 10, 'accommodation': 3, 'nearby': 6}
    message = [['amenities','none','projectType'],['possession','price'],['specifications'],['size','security','rating']]
    response = [[1,2,1],[0,1],[1],[0,1,1]]
    feature_order = {}
    #print create_new_chat_entry(feature_order,message,default_order)
    for i in range(len(message)):
        add_to_csv_file(message[i],response[i],18)
    Q = pd.read_csv('Q_order_CSV2.csv',header=0,index_col=0)
    A = pd.read_csv('answers_CSV2.csv',header=0,index_col=0)
    


    
