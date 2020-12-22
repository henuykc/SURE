# -*- coding: utf-8 -*-
__author__ = "Manzoor Ali"
__email__ = "manzoor@campus-uni.ubp.de"
import functools
import os
import sys
import time
import codecs
import glob
from whoosh.analysis import RegexTokenizer
from whoosh.fields import Schema, TEXT
from whoosh.index import create_in, open_dir
from whoosh.query import *

from nltk.corpus import stopwords
from Sentence import Sentence
from nltk import word_tokenize, bigrams



bad_tokens = [",", "(", ")", ";", "''",  "``", "'s", "-", "vs.", "v", "'", ":", ".", "--"]
stopwords_list = stopwords.words('english')
not_valid = bad_tokens + stopwords_list

headquarters = ['founder', 'co-founder', 'cofounder', 'co-founded', 'cofounded', 'founded',
                    'founders','started by']
def extract_bigrams(words):
    
    return [gram[0]+' '+gram[1] for gram in bigrams(words)]
def timecall(f):
    @functools.wraps(f)
    def wrapper(*args, **kw):
        start = time.time()
        result = f(*args, **kw)
        end = time.time()
        print("%s %.2f seconds" % (f.__name__, end - start))
        return result
    return wrapper


def create_index():
    regex_tokenize = re.compile('\w+(?:-\w+)+|<[A-Z]+>[^<]+</[A-Z]+>|\w+', re.U)
    tokenizer = RegexTokenizer(regex_tokenize)
    schema = Schema(sentence=TEXT(stored=True, analyzer=tokenizer))
    if not os.path.exists("index_founder"):
        os.mkdir("index_founder")
        idx = create_in("index_founder", schema)
    else:
        idx = open_dir("index_founder")
    return idx


@timecall
def index_sentences(writer):
    count = 0
    bad = 0
    not_f = 0
    max_tokens = 7
    min_tokens = 1
    context_window = 2
    #path = 'Wiki_Dump_June_01_20/cleanSmall/'
    path = 'Wiki_Dump_June_01_20/'
    for filename in glob.glob(os.path.join(path, '*.txt')):
       # with open(os.path.join(os.curdir(), filename), 'r') as f:
        f = codecs.open(str(filename), "r", "utf-8")
        for l in f:
            if count > 2:
                if ch == False:
                    not_f = not_f + 1
            ch = False
            try:
                words = word_tokenize(l)
                bi = extract_bigrams(words)
                if(len(words) < 5):
                    bad = bad + 1
                    continue
                for h in headquarters:
                    if ch:
                        continue
                    if (h in words) or (h in bi):
                        writer.add_document(sentence=l.strip())
                        ch = True
                        count += 1
                    else:
                        
                        continue
                    
            except UnicodeDecodeError as e:
                    print(e)
                    print(l)
                    sys.exit(0)
           
                
            
            if count % 100000 == 0:
                print(count, "lines processed")
            if bad % 1000000 == 0:
                print(bad, "lines less than 5")
            if not_f % 1000000 == 0:
                print(not_f, "lines rejected")
    print(f"{count} is total processed {bad} is less than 5 and {not_f} is rejected")
    f.close()
    writer.commit()


def main():
    idx = create_index()
    writer = idx.writer(limitmb=4096, procs=7, multisegment=True)
    index_sentences(writer)
    idx.close()


if __name__ == "__main__":
    main()
