#!/usr/bin/python3
import math
import os
from random import sample
import pickle as pickle
from tqdm import tqdm
from scipy.spatial.distance import cdist
import json
import numpy as np
import indicoio
from texttable import Texttable
indicoio.config.api_key = '51be63f44998d6bd83a785da695a5176'
import codecs
import sys
import time
#import scrapy

question =sys.argv[1]
with codecs.open("MI_Pass.txt","r",encoding='utf-8',errors='ignore') as file:
 _file=file.readlines()

questions=[]
answers=[]
ques=[]
ans=[]
for i in range(len(_file)):
    if(i%2==0):
        questions.append(_file[i])
    else:
        answers.append(_file[i])

num_questions=len(questions)
'''for i in range(num_questions):
    if(i>=int(sys.argv[2]) and i<int(sys.argv[3])):
        ques.append(questions[i])
for i in range(num_questions):
    if(i>=int(sys.argv[2]) and i<int(sys.argv[3])):
        ans.append(answers[i])
num_question=len(ques)        
for i in range(num_question):
    a=ques[i]
    ques[i]=a[:-1]

for i in range(num_question):
    a=ans[i]
    ans[i]=a[:-1]

faqs={}
for i in range(num_question):
    faqs[ques[i]]=ans[i]
'''    
for i in range(num_questions):
    a=questions[i]
    questions[i]=a[:-1]

for i in range(num_questions):
    a=answers[i]
    answers[i]=a[:-1]

faqs={}
for i in range(num_questions):
    faqs[questions[i]]=answers[i]
#print(len(faqs))

def make_feats(data):
    xrange=range
    chunks = [data[x:x+100] for x in xrange(0, len(data), 100)]
    feats = []

    for chunk in (chunks):
        feats.extend(indicoio.text_features(chunk))
        print(len(feats))

    return feats

def calculate_distances(feats):
  
    distances = cdist(feats, feats, 'cosine')
    return distances

def similarity_text(idx, distance_matrix, data, n_similar=num_questions+1):
    #print(num_questions)
    temp = Texttable()
    temp.set_cols_width([50, 20])

    sorted_distance_idxs = np.argsort(distance_matrix[idx])[:n_similar] 
    most_sim_idx = sorted_distance_idxs[1]

   
    temp.add_rows([['Text', 'Similarity']])
  ##  print temp.draw()
    
  
    faq_match = None
    coin=0;
    f=open("outfile1.txt",'w')
    f.close()
    for similar_idx in sorted_distance_idxs:
       
        datum = data[similar_idx]
        '''fix= open("mytext2.txt",'w+')

        fix.write(datum)
        fix.close()'''
        #print(datum)
        distance = distance_matrix[idx][similar_idx]

        
        similarity =  1 - distance
     
        #print(similarity)
        if(coin==0):
            None
        
        else:
             #print(faqs[datum])
             f=open("outfile1.txt",'a')
             #f.append(similarity)
             #f.write('coin\n')
             #print('1')
             #print(faqs[datum])
             f.write(faqs[datum]+"\n")
        coin=coin+1;
        temp.add_rows([[datum, str(round(similarity, 2))]])
    ##    print temp.draw()
        

        if similar_idx == most_sim_idx and similarity >= 0.00:
                    faq_match = data[most_sim_idx]
        else:
                sorry = "Sorry, I'm not sure how to respond. Let me find someone who can help you."
    if faq_match is not None:
             print ("A: %r" % faqs[faq_match])
    else:
            print ("sorry")

def input_question(data, feats):
    if question is not None:
        data.insert(0, question)
    new_feats = indicoio.text_features(question)
    feats.insert(0, new_feats)
    return data, feats

def run():
    #print ('rrr')

    data = list(faqs.keys())
    #print (data)
    #print ("FAQ data received. Finding features.<br>")
    feats=make_feats(data)
    with open('faq_feats.pkl', 'wb') as f:
        pickle.dump(feats, f)
    #print ("FAQ features found!<br>")

    with open('faq_feats.pkl', 'rb') as f:
            feats = pickle.load(f)
    #print ("Features found -- success! Calculating similarities...<br>")

    input_results = input_question(data, feats)
    new_data = input_results[0]
    new_feats = input_results[1]
    distance_matrix = calculate_distances(new_feats)
    #print ("Similarities found. Generating table.<br>")

    idx = 0
    similarity_text(idx, distance_matrix, new_data)
    print ('<br>' + '-' * 80)

if __name__ == "__main__":
    
    run()
    

