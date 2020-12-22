# -*- coding: utf-8 -*-
#--------------------To Do------------------------------#
# Precision(P) = (System output(S) ^ database[Wikidata](D) ) / S
# Recall (R) = (System output(S) ^ database[Wikidata](D) ) / (System output(S) ^ database[Wikidata](D) ) U (D ^ Corpus(G))
# F1 = (2. P.R) / P + R

import fileinput
import glob
import pandas as pd
import codecs
import query_index
import kb
import sys
import candidate_sentences
import string

all_dict = {}
def process_wiki():
    pass    
    
def cal_pmi(not_in_db,rel_type,df_cent_all):
    pass
def calculate_c(rel_type,S):
    database  = {}
    not_database = {}
    true_not_indb ={}
    d = 0
    c = 0
    with open('selected_head.txt',"r") as file1:
        sys.stdout.flush()
        for l in file1:
          
          _,_,all_en = candidate_sentences.Sentence(l.strip(),"ORG","LOC",7,1,2)
          all_dict.update(all_en)
        print('Total Extracted from dataset',len(all_dict.keys()))
    for k in all_dict.keys():
        if k in S.keys():
            continue
        if kb.exist_kb_recall(k,rel_type) == 1:
            database[k] = 1
            c += 1
        else:
            not_database[k] = 0
    
    #c = len(database)
    #print('found in KB ',len(database))
# ==========================To increase performance and f1===================================================
#     for k in not_database.keys():
#         pmi = query_index.proximity_pmi_rel_word(k[0],k[1],rel_type,12,3,2)
#         if pmi > 0 :
#             true_not_indb[k] = pmi 
#             d += 1
# =============================================================================
    return c,d

def process_output(data,threshold,rel_type):
    system_output = dict()
    l = list()
    count = 0
    for line in fileinput.FileInput(data):
        if line.startswith('instance'):
            instance_parts, score = line.split("score:")
            e1, e2 = instance_parts.split("instance:")[1].strip().split('\t')

        if line.startswith('sentence'):
            sentence = line.split("sentence:")[1].strip()
        if line.startswith('pattern_bef:'):
            bef = line.split("pattern_bef:")[1].strip()

        if line.startswith('pattern_bet:'):
            bet = line.split("pattern_bet:")[1].strip()

        if line.startswith('pattern_aft:'):
            aft = line.split("pattern_aft:")[1].strip()
        if line.startswith('\n') and float(score) >= threshold:
           
            system_output[(e1,e2)] = (bef,bet,aft)
        
    return  system_output


def main():
    threhsold = 0
    database = {}
    not_database = {}
    true_not_indb = {}
    rel_type = "headquarter" 
    S = process_output('Extras/rel_birthplace.txt',threhsold,rel_type)

    print('system output',len(S))
    
    print('checking in knowledge base...')
    for k in S.keys():
        sub = str(k[0]).replace('_',' ')
        obj = str(k[1]).replace('_', ' ')
        sub = string.capwords(sub)
        obj = string.capwords(obj)
        tup = (sub,obj)
        print(tup)
       
        database[k] = kb.exist_kb_pre(tup,rel_type)
    
    for k,v in database.items():
        if v == 0:
            not_database[k] = v
    print('Not found in KB ',len(not_database))
    
# =============================================================================
#     for k in not_database.keys():
#         pmi = query_index.proximity_pmi_rel_word(k[0],k[1],rel_type,18,4,4)
#         if pmi > 0 :
#             true_not_indb[k] = pmi 
#     print('True but not foud in db ',len(true_not_indb))
#     presison = (len(true_not_indb) + (len(S) - len(not_database))) / len(S)
#     print('The system accuracy for ',rel_type,'  =  ',presison)
# #=============================================================================
#     c,d = calculate_c(rel_type,S)
#     print('found in db = ',c,' Correct but not found in db not in sys_output = ',d)
#     recall = (len(true_not_indb) + (len(S) - len(not_database))) / (len(true_not_indb) + (len(S) - len(not_database)) + c)
#     print('System recall for ',rel_type,' = ',recall)
#     f1 = 2 * (presison * recall) / (presison + recall)
#     print('The system f1 score = ', f1)
# =============================================================================
#=============================================================================
        
    #print(database)
    
    #print(S)

if __name__ == "__main__":
    main()
