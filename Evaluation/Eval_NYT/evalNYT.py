# -*- coding: utf-8 -*-
__author__ = "Manzoor Ali"
__email__ = "manzoor@campus-uni.ubp.de"
import fileinput
import pandas as pd
import boot_straping.kb as kb
import codecs
import sys, os


location = ['location','country','city','state_or_province' ]
def process_output(data,threshold,rel_type):
    system_output = dict()
    
    l = list()
    count = 0
    check = {}
    correct = 0
    for line in fileinput.FileInput(data):
        if line.startswith('instance'):
            instance_parts, score = line.split("score:")
            e1, e2 = instance_parts.split("instance:")[1].strip().split('\t')
            e1 = str(e1).lower()
            e2 = str(e2).lower()
            e1 = e1.replace(" ","_")
            e2 = e2.replace(" ","_")

        if line.startswith('sentence'):
            sentence = line.split("sentence:")[1].strip()
            sent_parts = sentence.split('\t')
            if sent_parts[3].strip() == rel_type:
                correct += 1
                
                
        if line.startswith('pattern_bef:'):
            bef = line.split("pattern_bef:")[1].strip()

        if line.startswith('pattern_bet:'):
            bet = line.split("pattern_bet:")[1].strip()

        if line.startswith('pattern_aft:'):
            aft = line.split("pattern_aft:")[1].strip()
        if line.startswith('\n') and float(score) >= threshold:
            count += 1
            system_output[(e1,e2)] = (bef,bet,aft)
            check[sentence] = (e1,e2)
        
    return  len(system_output) ,len(check), count
def unique_relation(rel_type):
    count  = 0
    uniq_dict = {}
    duplicate = 0
    total = 0
    filename = os.path.abspath('data/AnnotatedANLP_NYT__sample.txt')
    print(filename)
    with codecs.open(filename,'r', encoding='utf-8',
                 errors='ignore') as fdata:
        for line in fdata.readlines():
            
    
        
            l = line.split('\t')
            if l[3].strip() == rel_type:
                total += 1
                tup = (l[0].strip(),l[1].strip())
                if tup in uniq_dict:
                    duplicate += 1
                else:
                    uniq_dict[tup] = 'dummy'
            count += 1
    
    return len(uniq_dict),total
        
def recall(rel_type):
    dictAll = {}
    for line in fileinput.FileInput('data/AnnotatedANLP_NYT__sample.txt'):
        l = line.split('\t')
        e1 = l[0]
        e2 = l[1]
        rel = l[3]
        if rel.strip() == rel_type.strip():
            if (e1,e2) in dictAll.keys():
                continue
            else:
                dictAll[(e1,e2)] = rel
        
    return len(dictAll)
        
        
        

def extract_realtion(rel_type,name):
    count = 0
    subject = ''
    save = False
    file1 = open(name+'_Relation.txt', 'w')
    for line in fileinput.FileInput('cleanNYTtrain.txt'):
        
        if line.startswith(' sub:'):
            e_sub = line.split("\t")
            subject = e_sub[1].strip()
            sub_type = e_sub[3].strip()
           
            if  sub_type == 'NA':
                subject = ''
                continue
        if line.startswith(' obj:'):
            e_obj = line.split('\t')
            obj = e_obj[1].split(' ')
            obj_type = e_obj[2].strip()
            objct = obj[1]
            if obj_type == 'NA':
                objct = ''
                continue
        if line.startswith(' rel:'):
            rel = line.split('\t')
            relation = rel[1].strip()
            if relation == 'NA':
                relation = ''
                continue
            elif relation == rel_type and sub_type == 'person':
                if obj_type in location:
                    save = True
                    count += 1
            else:
                save = False
        if line.startswith(' sent:'):
            sent = line.split('\t')
            sent = str(sent[1])
            if save:
                line1 = str(subject+'\t'+objct+'\t'+relation+'\n')
                file1.write(line1)
                file1.write(sent)
                save = False
    file1.close()
    print('Total number of birth palce relation = ',count)
def main():
   
    rel_type = '/people/person/place_of_birth'
    name = 'place_of_birth'
    
    #extract_realtion(rel_type,name)
    nyt_rel,total = unique_relation(rel_type)
    print(f'unique = {nyt_rel} and total = {total}')
    S , correct , count= process_output('data/output_relationship.txt',0,rel_type)
    print(f'unique output = {S} and all = {count}')
   # print(f'correct = {correct}')
    all_dataset = recall(rel_type)
    print(f'All from dataset = {all_dataset}')
    recal = round(S / (total) , 3)
    recal2 = round(count / all_dataset,3)
    print('recall',recal)
    #print(f'Total System Output = {S}')
    per = round(S / nyt_rel , 3)
    print(f'precision = {per}')
    #rec = S / total
    #print(f'recall = {rec}')
    f1 = 2 * round((per * recal) / (per + recal), 3)
    print('f1 score = ',f1)
    #f2 = 2 * round((per * recal2) / (per + recal2), 3)
    #print(f'{per} & {recal2} & {f2} ')
    #print(f'{per} & {recal} & {f1} ')
    #print(f'All = {recall(rel_type)}')
        
if __name__ == "__main__":
    main()