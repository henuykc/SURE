# -*- coding: utf-8 -*-
__author__ = "Manzoor Ali"
__email__ = "manzoor@campus-uni.ubp.de"
# pip install torch torchvision
# pip install -U sentence-transformers
from sentence_transformers import SentenceTransformer, util 
import numpy as np
import nltk
import sys
nltk.download('punkt')
import re
import cluster as cl

def sent_embeding(sentences):
    model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')
    sentence_embeddings = model.encode(sentences)
    return sentence_embeddings


def similirity(cluster,queries,cent, k=7, threshold = 0.9):
    patterns = {}
    paterns_pharses = []
    embedder = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')
    corpus_embeddings = embedder.encode(cluster, convert_to_tensor=True)
    if cent:
        for query in queries:
            query_embedding = embedder.encode(query, convert_to_tensor=True)
            cos_scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0]
            cos_scores = cos_scores.cpu()
            top_results = np.argpartition(-cos_scores, range(k))[0:k]
            for idx in top_results[0:k]:
                if cos_scores[idx] > threshold:
                    t = re.findall(r"[-+]?\d*\.\d+|\d+",str(cos_scores[idx]) )
                    score = float(t[0])
                    patterns[cluster[idx].strip()] = score
                    paterns_pharses.append(cluster[idx].strip())
    else:
        for query, value in queries.items():
            query_embedding = embedder.encode(query, convert_to_tensor=True)
            cos_scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0]
            cos_scores = cos_scores.cpu()
            top_results = np.argpartition(-cos_scores, range(k))[0:k]
            for idx in top_results[0:k]:
                if cos_scores[idx] > threshold:
                    t = re.findall(r"[-+]?\d*\.\d+|\d+",str(cos_scores[idx]) )
                    score = float(t[0])        
                    patterns[cluster[idx].strip()] = score - (1 - value)
                    paterns_pharses.append(cluster[idx].strip())
    return patterns, paterns_pharses
def similirity_extract(pat,sent,k=1, threshold = 0.5):
    find = False
    embedder = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')
    pat_embed = embedder.encode(pat, convert_to_tensor=True)
    sent_embed= embedder.encode(sent,convert_to_tensor=True)
   
        
    cos_scores = util.pytorch_cos_sim(pat_embed, sent_embed)[0]
    cos_scores = cos_scores.cpu()
    top_results = np.argpartition(-cos_scores, range(k))[0:k]
    for idx in top_results[0:k]:
        print(cos_scores[idx])
        if cos_scores[idx] > threshold:
                find = True

    return find






