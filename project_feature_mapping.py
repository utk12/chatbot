import json
import numpy as np
from elasticsearch import Elasticsearch
from update_question_features import convert_underscore_to_camelcase

def project_type_matching(p_data,p_features):
    data = p_data['projectDetails']['projectType']
    for key in p_features['projectType']['children']:
        p_features['projectType']['children'][key]['foundValue'] = data[key]
    return p_features

def possession_matching(pos,p_features):
    p_features['possession']['children'][pos]['foundValue'] = 1
    return p_features

def amenities_matching(p_data,p_features):
    sports = p_data['sportsActivities']
    club_house = p_data['clubHouse']
    
    for key in p_features['amenities']['children']:
        if key in sports:
            p_features['amenities']['children'][key]['foundValues'] = sports[key]
        if key in club_house:
            p_features['amenities']['children'][key]['foundValue'] = club_house[key]
    return p_features

def unit_details_matching(p_data,p_features):
    unit_ids = p_data['units']
    
    for unit in unit_ids:
        p_type = unit_ids[unit]['configurations']['type']       # type has info about property type like 2BHK etc
        p_type = '2BHK'      # comment this later
        p_features['accommodation']['children'][p_type]['foundValue'] = 1
        specs = unit_ids[unit]['specifications']
        return specs
        for s in specs:
            if s in p_features['specifications']['children']:
                p_features['specifications']['children'][s]['foundValue'] = specs[s]
    other_data = p_data['other']
    p_features['specifications']['children']['powerBackup']['foundValue'] = other_data['powerBackup']
    p_features['specifications']['children']['maintenance']['foundValue'] = other_data['maintenance']
    
    p_features['specifications']['children']['parking']['foundValue'] = p_data['projectDetails']['carParking']
    p_features['specifications']['children']['visitorParking']['foundValue'] = p_data['projectDetails']['visitorCarParking']
    p_features['specifications']['children']['vastuCompliant']['foundValue'] = p_data['projectDetails']['vastuCompliant']
    
    if p_data['projectDetails']['lifts']['max'] != 0:
        p_features['specifications']['children']['lift']['foundValue'] = 1
    else:
        p_features['specifications']['children']['lift']['foundValue'] = 0
    
        return p_features

def get_security_features(p_data):
    security_features = {}
    security_data = p_data['security']
    security_features['stickersForVehicles'] = security_data['stickersForVehicles']
    security_features['tagsForVehicles'] = security_data['tagsForVehicles']
    
    for key in security_data:
        if key in ['mainGate','tower']:
            gt_features = security_data[key]
            for feature in gt_features:
                value = gt_features[feature]
                if feature == 'guard':
                    feature = 'guards'
                s_key = convert_underscore_to_camelcase(feature+'_'+key.lower())
                security_features[s_key] = value
    del security_features['accessControlledTower']
    return security_features

def security_features_matching(p_data,p_features):
    features = get_security_features(p_data)
    for key in features:
        p_features['security']['children'][key]['foundValues'] = features[key]

    return p_features

def price_size_data(p_data):
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
                size[config_data['type']].append(config_data['superArea'])
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

def price_size_range_matching(p_data,p_features):
    price,size = price_size_data(p_data)
    price_range,size_range = price_size_range(price,size)
    
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

def all_project_feature_mapping(project_data,project_features):

    for pos in project_data:
        possession_data = project_data[pos]
        project_featues = possession_matching(pos,project_features)

        for project_id in possession_data:

            p_data = possession_data[project_id]
            project_features = project_type_matching(p_data,project_features)

            project_features = amenities_matching(p_data,project_features)

            project_features = unit_details_matching(p_data,project_features)

            project_features = price_size_range_matching(p_data,project_features)

            project_features = security_features_matching(p_data,project_features)
    return project_features

if __name__ == '__main__':

    es = Elasticsearch([{'host':'localhost','port':9200}])

    with open('Data/project_data.json') as open_file:
        es.index(index='project_data_index',doc_type='project_data_doc',id=1,body=json.load(open_file))

    with open('Data/project_features.json') as open_file:
        es.index(index='project_features_index',doc_type='project_features_doc',id=1,body=json.load(open_file))

    project_data = es.get(index='project_data_index',doc_type='project_data_doc',id=1)
    project_data = project_data['_source']

    project_features = es.get(index='project_features_index',doc_type='project_features_doc',id=1)
    project_features = project_features['_source']

    project_features = all_project_feature_mapping(project_data,project_features)