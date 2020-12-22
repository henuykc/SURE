# -*- coding: utf-8 -*-
__author__ = "Manzoor Ali"
__email__ = "manzoor@campus-uni.ubp.de"
from nltk.tokenize import sent_tokenize
import fileinput
from allennlp.predictors import Predictor
import pandas as pd
al = Predictor.from_path("https://s3-us-west-2.amazonaws.com/allennlp/models/fine-grained-ner-model-elmo-2018.12.21.tar.gz")
#text = "but the exhibition also includes a reproduction of an Odd Curio , a scale model of an '' Ideal Museum '' for the artist 's paintings designed in 1949 by the architect Peter Blake , a friend of Pollock 's who helped him install a show at the betty parsons gallery in Manhattan , long since closed"



def anotate(sen): 
    #tokens = sent_tokenize(sentence)
    #for t in tokens:
        S = al.predict(sentence=sen)
        s = "" 
        for w, tag in zip(S.get('words'), S.get('tags')):
           
            if tag == 'U-PERSON':
                s += ' <PER>'+w+'</PER>'
            elif  tag == 'U-GPE':
                s += ' <LOC>'+w+'</LOC>'
            elif  tag == 'U-ORG':
                s += ' <ORG>'+w+'</ORG>'
            elif tag == 'B-PERSON':
                s += ' <PER>'+w
            elif tag == 'L-PERSON':
                s += ' '+w+'</PER>'
            elif tag == 'B-GPE':
                s += ' <LOC>'+w
            elif tag == 'L-GPE':
                s += ' '+w+'</LOC>'
            elif tag == 'B-ORG':
                s += ' <ORG>'+w
            elif tag == 'L-ORG':
                s +=' '+w+'</ORG>'
            else:
                s += ' '+w
        return s    

def read_process_dataset():
    x = 0
    count = 0
    file1 = open('Annotated_AlenNLPNew.txt', 'w')
    df = pd.read_json(r'riedel_test.json',lines=True,chunksize=1)
   
    for c in df:
        x += 1
    
        sub = c['sub'].to_string(index=False)
        obj = c['obj'].to_string(index=False)
        sent = c.iloc[0,6]
        rel = c['rel'].to_string(index=False)
    
        if rel.strip() == 'NA':
            continue
        else:
            count += 1
            s = anotate(sent)
            file1.write(sub+'\t'+obj+'\t'+s+'\t'+rel+"\n")
        if count > 5:
            break
    
        if x > 1 and x % 1000 == 0:
            print(str(x))
    print('Total num of sentences ',str(x))
    print('Total relational sentences = ',str(count))
    file1.close()

def main():
    
    read_process_dataset()

if __name__ == "__main__":
    main()

    
