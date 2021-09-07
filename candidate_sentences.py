import re
from nltk import word_tokenize
from nltk.corpus import stopwords
# -*- coding: utf-8 -*-
bad_tokens = [",", "(", ")", ";", "''",  "``", "'s", "-", "vs.", "v", "'", ":", ".", "--"]
stopwords = stopwords.words('english')
not_valid = bad_tokens + stopwords
def select_sentences(text,e1_type,e2_type):
    '''Arguments: text = the file containing tagged sentences
                  e1_type = the type of first entity
                  e2_type = the type of second entity
        Returns:  entity_sentences_dict = The dictionary which have key value pairs the key represents entitis and 
                                        the value is the sentences containg the entities'''
    entity_sentences_dict = {}
    for l in text:
        types = []        
        pat = r'(?<=\<).+?(?=\>)'
        types = re.findall(pat, l)
        if len(types) >= 4 and types[0] == e1_type and types[2] == e2_type:
            tpl = tuple(re.findall('<[A-Z]+>([^<]+)</[A-Z]+>', l))
            if len(tpl) == 2:
                entity_sentences_dict[tpl] = l
            else:
                pass # todo: to split the sentence to multiple sentences based on the entity types to increase the recall
    return entity_sentences_dict

def find_locations(entity_string, text_tokens):
    locations = []
    e_parts = tokenize_entity(entity_string)
    for i in range(len(text_tokens)):
        if text_tokens[i:i + len(e_parts)] == e_parts:
            locations.append(i)
    return e_parts, locations

def tokenize_entity(entity):
    parts = word_tokenize(entity)
    if parts[-1] == '.':
        replace = parts[-2] + parts[-1]
        del parts[-1]
        del parts[-1]
        parts.append(replace)
    return parts
class EntitySimple:
    def __init__(self, _e_string, _e_parts, _e_type, _locations):
        self.string = _e_string
        self.parts = _e_parts
        self.type = _e_type
        self.locations = _locations

    def __hash__(self):
        return hash(self.string) ^ hash(self.type)

    def __eq__(self, other):
        return self.string == other.string and self.type == other.type



def Sentence( sentence, e1_type, e2_type, max_tokens, min_tokens,
             window_size, pos_tagger=None, config=None):
    #new code
    entity_sentences_dict = {}
    entity_between_dict = {}
    entity_all_dict = {}
    #end new code
    entities_regex = None
    entities_regex = re.compile('<[A-Z]+>[^<]+</[A-Z]+>', re.U)
    
    entities = []
    for m in re.finditer(entities_regex, sentence):
        entities.append(m)
    
    if len(entities) >= 2:
        # clean tags from text
        sentence_no_tags = None

        sentence_no_tags = re.sub(
                re.compile('</?[A-Z]+>', re.U), "", sentence
            )
        #print(sentence_no_tags)
        text_tokens = word_tokenize(sentence_no_tags)
        
        entities_info = set()
        for x in range(0, len(entities)):
            entity = entities[x].group()
            e_string = re.findall('<[A-Z]+>([^<]+)</[A-Z]+>', entity)[0]
            e_type = re.findall('<([A-Z]+)', entity)[0]
            e_parts, locations = find_locations(e_string, text_tokens)
            e = EntitySimple(e_string, e_parts, e_type, locations)
            entities_info.add(e)
        
        locations = dict()
        for e in entities_info:
            for start in e.locations:
                locations[start] = e
        sorted_keys = list(sorted(locations))
        #print(sorted_keys)
        count = 0
        select = 0
        for i in range(len(sorted_keys)-1):
            distance = sorted_keys[i+1] - sorted_keys[i]
            e1 = locations[sorted_keys[i]]
            e2 = locations[sorted_keys[i+1]]
            count = count + 1
            if max_tokens >= distance >= min_tokens and e1.type == e1_type and e2.type == e2_type:
                
                if e1.string == e2.string:
                    continue
                
                before = text_tokens[:sorted_keys[i]]
                before = before[-window_size:]
                between = text_tokens[sorted_keys[i] +
                                           len(e1.parts):sorted_keys[i+1]]
               
                after = text_tokens[sorted_keys[i+1]+len(e2.parts):]
                after = after[:window_size]
                if all(x in not_valid for x in
                       text_tokens[sorted_keys[i] + len(e1.parts):sorted_keys[i + 1]]):
                    continue
                #t = e1.string+','+e2.string
                t = tuple((e1.string,e2.string))
               
                #btw = ' '.join(before) + ' '+ e1.string+' ' +' '.join(between) +' '+ e2.string+' ' + ' '.join(after)
                btw = ' '.join(between)
                bef = ' '.join(before)
                aft = ' '.join(after)
                all_part = tuple((bef,btw,aft))
                #print(btw)
                entity_sentences_dict[t] = sentence
                entity_between_dict[t] = btw
                entity_all_dict[t] = all_part
                
    return entity_sentences_dict,entity_all_dict
                
                
