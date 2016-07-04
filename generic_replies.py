# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 16:17:33 2016
@author: Utkarsh
"""

#==============================================================================
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pandas as pd
import math,string,time,sys

pd.set_option('expand_frame_repr', False)
data = pd.read_csv('Data/data3.csv')
data = pd.DataFrame(data)

#print(data)
#==============================================================================
#Creating a dictionary of words from nltk corpus with freq 0
#==============================================================================
# from nltk.corpus import words
# word_list=words.words()
# print(word_list[1:10])
# vector_dict={}
# for word in word_list:
#     vector_dict[word]=0
#==============================================================================
relevant_dict={}
irrelevant_dict={}
# Creating a dictionary of relevent and non-relevent document words.
relevant_data = data.loc[data['Relevant']=='Yes']
irrelevant_data = data.loc[data['Relevant']=='No']

def remove_punct(str1):
    str2 = ''
    for l in str1:
        if l not in string.punctuation:
            str2 += l
        else:
            str2 += ' '
    return str2

def get_Rel_Frequency(word):
    if word in relevant_dict:
        return relevant_dict[word]
    else:
        return 0
def get_Irr_Frequency(word):
    if word in irrelevant_dict:
        return irrelevant_dict[word]
    else:
        return 0
def remove_stopwords(str):
    stop_words = set(stopwords.words("english"))
    tokens = word_tokenize(str)
    filtered_tokens = [w for w in tokens if w not in stop_words]
    return filtered_tokens
#==============================================================================
#Building relevant_dict
def build_relevant_dict():    
    for document in relevant_data['User_query']:
        document = remove_punct(document)
        document_tokens = word_tokenize(document)
        for token in document_tokens:
            token=token.lower()
            relevant_dict[token] = get_Rel_Frequency(token) + 1        
build_relevant_dict()
#==============================================================================
#Building irrelevant_dict
def build_irrelevant_dict():   
    for document in irrelevant_data['User_query']:
        document = remove_punct(document)
        document_tokens=word_tokenize(document)
        for token in document_tokens:
            token=token.lower()
            irrelevant_dict[token] = get_Irr_Frequency(token) + 1
build_irrelevant_dict()
#==============================================================================
#print(data)
#print(len(data.index)) #52
#print(irrelevant_dict['live'])        
#print('++++++++++++++++++++++')
#==============================================================================
# print(get_Rel_Frequency('gurgaon'))
# print(get_Irr_Frequency('gurgaon'))
# print(get_Rel_Frequency('weather'))
# print(get_Irr_Frequency('weather'))
#==============================================================================
def get_Word_Score(word):
    #Handle the error when word is not in both he dictionaries DivisionByZeroError
    if((get_Rel_Frequency(word)+get_Irr_Frequency(word))==0):
        final_score = 0
    else:
        relevant_score = get_Rel_Frequency(word)/(get_Rel_Frequency(word)+get_Irr_Frequency(word))
        irrelevant_score=get_Irr_Frequency(word)/(get_Rel_Frequency(word)+get_Irr_Frequency(word))
        max_score=max(relevant_score,irrelevant_score)
        if max_score == relevant_score:
            final_score = (max_score-0.5)*2
        elif max_score == irrelevant_score:
            final_score = -((max_score-0.5)*2)
    #range of final_score = {-1,1}
    return final_score
#==============================================================================
# Calculating a score for each term in a document and returning a vector for the document
#doc_vector={}
def doc_to_vector(str):
    doc_vector={}
    str=remove_punct(str)
    doc_tokens=word_tokenize(str)
    for word in doc_tokens:
        word=word.lower()
        doc_vector[word] = get_Word_Score(word) #returns final_score
    return doc_vector
#==============================================================================
# Calculate cosine of two vectors
def get_cosine(vec1,vec2):
    intersection = list(set(vec1.keys()) & set(vec2.keys()))
    numerator = sum([vec1[x] * vec2[x] for x in intersection])
    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator
#==============================================================================
#get most similar query
def get_msim_query(str):
    max_cosine = -1
    for document in data['User_query']:
        temp_cosine = get_cosine(doc_to_vector(document),doc_to_vector(str))
        if max_cosine < temp_cosine:
            max_cosine = temp_cosine
            matched_document = document
    return matched_document
    
def get_reply(str):
    return data.Bot_reply[data.User_query == get_msim_query(str)].values[0]
    
def get_relevancy(str):
    return data.Relevant[data.User_query == get_msim_query(str)].values

#print(get_Rel_Frequency('gurgaon'))
#print(get_Irr_Frequency('gurgaon'))
#print(get_Word_Score('weather'))

#==============================================================================
# doc1 = 'Show me the weather in Gurgaon.'
# print(doc_to_vector(doc1))
# doc2 = 'Show me a place in Gurgaon.'
# print(doc_to_vector(doc2))
# print(get_cosine(doc_to_vector(doc1),doc_to_vector(doc2)))
# doc3 = 'Do you have properties to buy?'  
# doc4 = 'Hello !'
#==============================================================================
#print(get_cosine(doc_to_vector(),doc_to_vector()))
#==============================================================================
# print(get_msim_query(doc4))
# print(get_reply(doc4))
# print(get_relevancy(doc4))
#==============================================================================
def sleep(n):
    for i in range(n):
        time.sleep(1)
        print '.',
        sys.stdout.flush()
    print('bye!!')

#==============================================================================
if __name__ == '__main__':
    print('Hey there ! Enter a query to chat.\n')
    while(True):
        inp = raw_input()
        if inp == 'Bye' or inp == 'bye':
            print 'Have a good day.',
            sleep(3)
            break
        print(get_reply(inp))
#==============================================================================