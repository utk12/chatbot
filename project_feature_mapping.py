import json
import copy
import numpy as np
from elasticsearch import Elasticsearch
#from update_question_features import convert_underscore_to_camelcase

def convert_underscore_to_camelcase(text):
	components = text.split('_')
	return components[0] + "".join(x.title() for x in components[1:])

def convert_space_to_underscore(str):
	return ''.join(map(lambda x:x.lower() if x != ' ' else "_",str))


def project_type_matching(p_data,p_features):

    if 'projectType' in p_data['projectDetails']:
        data = p_data['projectDetails']['projectType']
        for key in p_features['projectType']['children']:
            if key in data:
                p_features['projectType']['children'][key]['foundValue'] = 1
            else:
                p_features['projectType']['children'][key]['foundValue'] = 0
    else:
        for key in p_features['projectType']['children']:
            p_features['projectType']['children'][key]['foundValue'] = 0

    if 'carParking' in p_data['projectDetails']:
        p_features['specifications']['children']['parking']['foundValue'] = 1
    else:
        p_features['specifications']['children']['parking']['foundValue'] = 0

    if 'visitorCarParking' in p_data['projectDetails']:
        p_features['specifications']['children']['visitorParking']['foundValue'] = 1
    else:
        p_features['specifications']['children']['visitorParking']['foundValue'] = 0

    if 'vastuCompliant' in p_data['projectDetails']:
        p_features['specifications']['children']['vastuCompliant']['foundValue'] = 1
    else:
        p_features['specifications']['children']['vastuCompliant']['foundValue'] = 0

        
    return p_features

def possession_matching(pos,p_features):
    #print p_features.keys()
    for key in p_features['possession']['children']:
        if key == pos:
            p_features['possession']['children'][key]['foundValue'] = 1
        else:
            p_features['possession']['children'][key]['foundValue'] = 0
    return p_features


def amenities_matching(p_data,p_features):
    if 'sportsActivities' in p_data:
        sports = p_data['sportsActivities']
    else:
        sports = {}

    if 'clubHouse' in p_data:
        club_house = p_data['clubHouse']
    else:
        clubHouse = {}
    
    for key in p_features['amenities']['children']:
        if key in sports:
            p_features['amenities']['children'][key]['foundValue'] = 1
        elif key in club_house:
            p_features['amenities']['children'][key]['foundValue'] = 1
        else:
            p_features['amenities']['children'][key]['foundValue'] = 0
    return p_features


def unit_details_matching(p_data,p_features):
    unit_ids = p_data['units']
    
    for unit in unit_ids:
        p_type = unit_ids[unit]['configurations']['type']       # type has info about property type like 2BHK etc
        p_type = '2BHK'      # comment this later
        p_features['accommodation']['children'][p_type]['foundValue'] = 1

        if 'specifications' in unit_ids[unit]:
            specs = unit_ids[unit]['specifications']
            for key in p_features['specifications']['children']:
                if key in specs:
                    p_features['specifications']['children'][key]['foundValue'] = 1
                else:
                    p_features['specifications']['children'][key]['foundValue'] = 0
        else:
            for spec in p_features['specifications']['children']:
                p_features['specifications']['children'][spec]['foundValue'] = 0
                
    if 'other' in p_data:
        other_data = p_data['other']
        p_features['specifications']['children']['powerBackup']['foundValue'] = 1
        p_features['specifications']['children']['maintenance']['foundValue'] = 1
    else:
        p_features['specifications']['children']['powerBackup']['foundValue'] = 0
        p_features['specifications']['children']['maintenance']['foundValue'] = 0

    if 'lifts' in p_data['projectDetails'] and p_data['projectDetails']['lifts']['max'] != 0:    
        p_features['specifications']['children']['lift']['foundValue'] = 1
    else:
        p_features['specifications']['children']['lift']['foundValue'] = 0
    
    return p_features

def get_security_features(p_data):
    security_features = {}
    if 'security' in p_data:
        security_data = p_data['security']
        if 'stickersForVehicles' in security_data:
            security_features['stickersForVehicles'] = 1
        else:
            security_features['stickerVehicles'] = 0
        if 'tagsForVehicles' in security_data:
            security_features['tagsForVehicles'] = 1
        else:
            security_features['tagsForVehicles'] = 0
    
        for key in security_data:
            if key in ['mainGate','tower']:
                gt_features = security_data[key]
                for feature in gt_features:
                    if feature == 'guard':
                        feature = 'guards'
                    s_key = convert_underscore_to_camelcase(feature+'_'+key.lower())
                    security_features[s_key] = 1
        
        #del security_features['accessControlledTower']
    return security_features

def security_features_matching(p_data,p_features):
    features = get_security_features(p_data)
    for key in p_features['security']['children']:
        if key in features:
            p_features['security']['children'][key]['foundValue'] = 1
        else:
            p_features['security']['children'][key]['foundValue'] = 0
    
    return p_features

def price_size_data(p_data):    # p_data has complete data of all projects
    price = {}
    size = {}
    for p_id in p_data:            #  Iterating through all project ids
        unit_data = p_data[p_id]['units']
        for unit_id in unit_data:
            config_data = unit_data[unit_id]['configurations']
            if config_data['type'] in price:
                price[config_data['type']].append(config_data['price'])
            else:
                price[config_data['type']] = [config_data['price']]
            
            if config_data['type'] in size:
                size[config_data['type']].append(config_data['superArea'])
            else:
                size[config_data['type']] = [config_data['superArea']]
    return price,size

def price_size_range(price,size):
    price_range ={}
    size_range = {}
    
    for key in price:
        price_L = min(price[key]) + (max(price[key]) - min(price[key]))/3
        price_H = min(price[key]) + 2*(max(price[key]) - min(price[key]))/3
        
        size_L = min(size[key]) + (max(size[key]) - min(size[key]))/3
        size_H = min(size[key]) + 2*(max(size[key]) - min(size[key]))/3
        
        price_range[key] = (price_L,price_H)
        size_range[key] = (size_L,size_H)
        
    return price_range,size_range

def price_size_range_matching(p_data,p_features,price_range,size_range):
    for unit_id in p_data['units']:
        config_data = p_data['units'][unit_id]['configurations']
        unit_price = config_data['price']
        unit_size = config_data['superArea']
        
        if unit_price > price_range[config_data['type']][1]:
            p_features['price']['children']['price_high']['foundValue'] = 1
        elif unit_price < price_range[config_data['type']][0]:
            p_features['price']['children']['price_low']['foundValue'] = 1
        else:
            p_features['price']['children']['price_medium']['foundValue'] = 1
            
        if unit_size > size_range[config_data['type']][1]:
            p_features['size']['children']['price_high']['foundValue'] = 1
        elif unit_size < size_range[config_data['type']][0]:
            p_features['size']['children']['size_low']['foundValue'] = 1
        else:
            p_features['size']['children']['size_medium']['foundValue'] = 1
            
    return p_features

def all_features_mapping(project_data,project_features,price_range,size_range):

    #p_data = project_data
    pos = convert_space_to_underscore(project_data['projectStatus'])
    pos = convert_underscore_to_camelcase(pos)
    
    project_features = possession_matching(pos,project_features)
    
    project_features = project_type_matching(project_data,project_features)
    
    project_features = amenities_matching(project_data,project_features)

    project_features = unit_details_matching(project_data,project_features)

    project_features = security_features_matching(project_data,project_features)    
        
    project_features = price_size_range_matching(project_data,project_features,price_range,size_range)
    
    return project_features



##def all_projects_mapping(project_data,project_features):
##
####    for pos in project_data:
####        possession_data = project_data[pos]
####        project_featues = possession_matching(pos,project_features)
##    price,size = price_size_data(project_data)
##    price_range,size_range = price_size_range(price,size)
##
##    for project_id in project_data:
##        p_features = copy.deepcopy(project_features)
##        project_features = all_features_mapping(project_data[project_id],p_features)
##        
##
##        return project_features

if __name__ == '__main__':

    es = Elasticsearch([{'host':'localhost','port':9200}])

    with open('1.json') as open_file:
        es.index(index='project_data_index',doc_type='project_data_doc',id=1,body=json.load(open_file))

    with open('project_features.json') as open_file:
        es.index(index='project_features_index',doc_type='project_features_doc',id=1,body=json.load(open_file))

    project_data = es.get(index='project_data_index',doc_type='project_data_doc',id=1)
    project_data = project_data['_source']['9999']['projects']

    project_features = es.get(index='project_features_index',doc_type='project_features_doc',id=1)
    project_features = project_features['_source']

    price,size = price_size_data(project_data)
    project_data = project_data['-KLLMK6AGsUeVWYUGAed']
    price_range,size_range = price_size_range(price,size)
    
    p_features = all_features_mapping(project_data,project_features,price_range,size_range)
    p_features = json.dumps(p_features)
    print p_features
    #print get_security_features(project_data)
    #print project_features.keys()
##    for pos in project_data['9999']['projects']:
##        print pos
    #p_features = all_features_mapping(project_data,project_features)
    #print 'project features:',p_features
