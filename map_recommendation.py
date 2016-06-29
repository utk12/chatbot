import copy
import numpy as np
import os
import pandas as pd

def countPairs(f):
    features = list(Q_data.columns)
    count = {}
    for i,n in enumerate(list(f)):
        if  n > 0:
            q = list(Q_data.ix[i])
            a = list(A_data.ix[i])
            if (n+1) <= max(q):
                pos = q.index(n+1)
                dict_name =  features[pos]
                if a[pos] >= 0 :
                    if dict_name in count:
                        count[dict_name] += a[pos]
                    else:
                        count[dict_name] = a[pos]
    return count

def formPairs(Q_data):
    features = list(Q_data.columns)
    pairs_occurences = {}
    for f in features:
        data = Q_data[f]
        pairs_occurences[f] = countPairs(data)
    #print pairs_occurences
    return pairs_occurences

def deleteAll(dictionary,f):
    del dictionary[f]
    for d in dictionary.values():
        if f in d:
            del d[f]
    return dictionary

def nextFeatureSuggestion(temp,feature):
    # print 'Current question is asked from which feature?'
    start = feature
    #print 'Question is being asked from this now'
    try:
        next_feature = max(temp[start],key=temp[start].get)
        # print 'Next best possible features to ask question from:'
        # print temp[start]
        temp = deleteAll(temp,start)
        return next_feature
    except:
        return None

def orderQuestions(temp):
    print 'Enter the feature to start with'
    start = raw_input()
    print "Question is being asked from %s now"%(start)
    try:
        for i in range(10):
            next_f = max(temp[start],key=temp[start].get)
            temp = deleteAll(temp,start)
            print next_f
            start = next_f
    except:
        print 'End of Loop'

if __name__ == '__main__':
    
    Q_data = pd.read_csv('Data/Q_order_CSV2.csv',header=0,index_col=0)
    A_data = pd.read_csv('Data/answers_CSV2.csv',header=0,index_col=0)

    pair_occurences = formPairs(Q_data)
    temp = copy.deepcopy(pair_occurences)
    print nextFeatureSuggestion(temp,'possession')
    #orderQuestions(temp)