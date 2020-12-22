# -*- coding: utf-8 -*-

from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh.index import open_dir, os
from whoosh.query import spans
from whoosh import query
from nltk import word_tokenize, bigrams


headquarters = ['headquarters','headquarter' ,'headquartered', 'offices', 'office',
                          'main building', 'building in', 'factory', 'plant in','headquarter in','headquarters in','based in', 'located in', 'main office', ' main offices',
                        'offices in', 'building in','office in', 'branch in',
                        'store in', 'firm in', 'factory in', 'plant in',
                        'head office', 'head offices', 'in central',
                        'in downtown', 'outskirts of', 'suburs of']

# =============================================================================
# headquarters = ['founder', 'co-founder', 'cofounder', 'co-founded', 'cofounded', 'founded',
#                     'founders','started by']
# =============================================================================
def extract_bigrams(words):
    
    return [gram[0]+' '+gram[1] for gram in bigrams(words)]
def tokenize_entity(entity):
    parts = word_tokenize(entity)
    if parts[-1] == '.':
        replace = parts[-2] + parts[-1]
        del parts[-1]
        del parts[-1]
        parts.append(replace)
    return parts

def find_locations(entity_string, text_tokens):
    locations = []
    e_parts = tokenize_entity(entity_string)
    for i in range(len(text_tokens)):
        if text_tokens[i:i + len(e_parts)] == e_parts:
            locations.append(i)
    return e_parts, locations
def calculate_distance(loc,loc2,window,before,after):
    previous_distance = window - (before + after)
    start = 0 
    end = 0    
    if len(loc) < len(loc2):
        for i in range(0,len(loc)):
            distance = abs(loc2[i] - loc[i])
            if distance > previous_distance:
                continue
            elif distance < previous_distance:
                start = loc[i] - before
                end = loc2[i] + after
                previous_distance = distance
    else:
        for i in range(0,len(loc2)):
            distance = abs(loc2[i] - loc[i])
            if distance > previous_distance:
                continue
            elif distance < previous_distance:
                start = loc[i] - before
                end = loc2[i] + after
                previous_distance = distance
    return start, end

def proximity_pmi_rel_word( entity1,entity2,rel_type,window,before,after):
    d = 0
    n = 0
    pmi = 0
    index =  ['index_150M','index_300M','index_450M','index_700M','index_1000M','index_abM']
    #index = ['index_founder']
    for x in index:
       
        idx = open_dir(x)
        count = 0
       
        q_limit = 500
        with idx.searcher() as searcher:
            try:
                query_wout_rel = entity1 +" " + entity2
               
                query = QueryParser("sentence", idx.schema).parse(query_wout_rel)
                denom = searcher.search(query, limit=q_limit)
                #print(len(denom))
                d = d + len(denom)
                #print(d)
                #print(d)
                for s in denom:
                    sentence = s.get("sentence")
                   # print(sentence)
                    words = word_tokenize(sentence)
                    #print('before ',len(words))
                    _,loc = find_locations(entity1,words)
                    _,loc2 = find_locations(entity2,words)
                    start, end = calculate_distance(loc,loc2,window,before,after)
                    words = words[start:end+1]
                    #print('after ',len(words))
                    if len(words) > 3:
                        bi = bigrams(sentence)
                        
                        ch = False
                        for h in headquarters:
                            if ch:
                                continue
                            if (h in words) or (h in bi):
                                count += 1
                                ch = True
                                
                            else:
                                continue
                    else:
                        continue
                        
                    
                #query_w_rel = entity1 +" " +rel_type +" "+ entity2
                #query = QueryParser("sentence", idx.schema).parse(query_w_rel)
                #nomerator = searcher.search(query, limit=q_limit)
                #print(len(nomerator))
                n = n + count
                #print(n)
            except:
                pass
    if d > 0:
        pmi = n / d
    return pmi            #print(len(hits))

            
#pmi = proximity_pmi_rel_word('European Union', 'New Zealand','headquarter')
#print(pmi)
#To Do
# PMI based on cloesness of enitity and the words found in between to completly satisfy the PMI definition                    