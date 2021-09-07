# -*- coding: utf-8 -*-
__author__ = "Manzoor Ali"
__email__ = "manzoor@campus-uni.ubp.de"
import sys
from nltk import word_tokenize,bigrams,ngrams 
import cluster as cl
import index
import candidate_sentences
import fileinput

def extract_bigrams(words):
    return [gram[0]+' '+gram[1] for gram in bigrams(words)]

def new_patterns(cluster,pharses,similiraty,top_k):
        s , p = index.similirity(cluster,pharses,False,top_k,similiraty) # explain
        return s,p
def exract_relations_sent(sentence_dict,unique_patterns,sent_with_enities,pat_score):
    f_output = open("Evaluation/Eval_NYT/data/output_relationship.txt", "w")
    for pat in unique_patterns:
        score = pat_score[pat]
        for key,value in sent_with_enities.items():
            text = value[0]+' '+value[1] +' ' +value[2]
            #print(text)
            if pat in text:
                f_output.write("instance: " + key[0]+'\t'+key[1]+'\tscore:'+str(score)+'\n')
                f_output.write("sentence: "+sentence_dict[key]+'\n')
                f_output.write("pattern_bef: "+sent_with_enities[key][0]+'\n')
                f_output.write("pattern_bet: "+sent_with_enities[key][1]+'\n')
                f_output.write("pattern_aft: "+sent_with_enities[key][2]+'\n')
                f_output.write("\n")
    f_output.close()

def extract_relations_window(sentence_dict,unique_patterns,all_dict,pat_score):
    
    f_output = open("Evaluation/Eval_NYT/data/output_relationship.txt", "w")
    for pat in unique_patterns:
        score = pat_score[pat]
        bi_pat = ngrams(pat.split(),2)
        for key,value in all_dict.items():
            text = value[0]+' '+value[1] +' ' +value[2]
            tokens = word_tokenize(text)    
            bgram = ngrams(text.split(), 2)
            pat_token = word_tokenize(pat)
            count = 0
            for pt_bi in bi_pat:
                
                for st_bi in bgram:
                    
                    if st_bi == pt_bi:
                        count += 1
            for pt in pat_token:
                for st in tokens:
                    if st == pt:
                        count += 0.5
            if count * score > 2:
                f_output.write("instance: " + key[0]+'\t'+key[1]+'\tscore:'+str(count*score)+'\n')
                f_output.write("sentence: "+sentence_dict[key]+'\n')
                f_output.write("pattern_bef: "+all_dict[key][0]+'\n')
                f_output.write("pattern_bet: "+all_dict[key][1]+'\n')
                f_output.write("pattern_aft: "+all_dict[key][2]+'\n')
                f_output.write("\n")
    f_output.close()

def main():
    if len(sys.argv) < 4:
        print('please enter annotated text, Head and Tail entities types e.g PER (for person) and number of cluster')
        sys.exit()
    input_data = sys.argv[1]
    eh_type = sys.argv[2]
    et_type = sys.argv[3]
    num_cluster = sys.argv[4]
    
    for line in fileinput.FileInput('config.txt'):
        if line.startswith('sentence_length:'):
            sentence_length = line.split("sentence_length:")[1].strip()
        if line.startswith('between_length:'):
            bet_length = line.split("between_length:")[1].strip()
        if line.startswith('before_after_window:'):
            bef_aft_length = line.split("before_after_window:")[1].strip()
        if line.startswith('top_similar:'):
            top_k = line.split("top_similar:")[1].strip()
        if line.startswith('similiraty:'):
            smlty = line.split("similiraty:")[1].strip()
        if line.startswith('query_term:'):
            query_term = line.split("query_term:")[1].strip()                      
   
    count = 0
    sent_with_enities = {}
    selected_sentences = []
    selected_patterns = []
    pat_score = {}
    sentence_dict = {}
    print(f'{input_data}, {eh_type}, {et_type}, {num_cluster}')
    with open(input_data) as file1:
        sys.stdout.flush()
        for line in file1:
          count += 1
          sen_en,sent_processed = candidate_sentences.Sentence(line.strip(),str(eh_type),str(et_type),int(sentence_length),int(bet_length),int(bef_aft_length)) # Change the values to variables accordingly
          sentence_dict.update(sen_en)
          sent_with_enities.update(sent_processed)
        print("No of selected candidate sentences from "+
              str(count)+" raw corpus are " +
              str(len(sent_with_enities))+" sentences")
        for l in sent_with_enities.values():
            l = l[0]+" " + l[1] +" "+ l[2]
            selected_sentences.append(l)
        encoding = index.sent_embeding(selected_sentences)
        clustered_sentences = cl.cluster(selected_sentences, encoding ,int(num_cluster)) 
        query_term = [query_term]
        for i, cluster in enumerate(clustered_sentences):
            print(f"Cluster # {i+1}")
            score , pharses = index.similirity(cluster,query_term,True,int(top_k),float(smlty))
            if len(pharses) > 0:
                selected_patterns.extend(pharses)
                pat_score.update(score)
                s,p =  new_patterns(cluster, score,float(smlty),int(top_k))
                selected_patterns.extend(p)
                pat_score.update(s)
        print(f'selected patterns {len(selected_patterns)}')
        unique_patterns = set(selected_patterns)
        print(f"Unique pattrens are {len(unique_patterns)}")
        exract_relations_sent(sentence_dict,unique_patterns,sent_with_enities,pat_score)

if __name__ == "__main__":
    main()
