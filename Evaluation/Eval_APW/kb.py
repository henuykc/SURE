# -*- coding: utf-8 -*-
__author__ = "Manzoor Ali"
__email__ = "manzoor@campus-uni.ubp.de"
import requests
from SPARQLWrapper import SPARQLWrapper, JSON
prefixes = """PREFIX dbo:<http://dbpedia.org/ontology/>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                PREFIX dbp:<http://dbpedia.org/resource/>"""

sparql = SPARQLWrapper("http://dbpedia.org/sparql")

def search_kb(tuples, endpoint = sparql ,prefixes= prefixes,):
    r = []
    try:
        query = """select ?lbl
                where {
                 <http://dbpedia.org/resource/"""+tuples[0].replace(" ", "_") +"""> 
                 ?p <http://dbpedia.org/resource/"""+tuples[1].replace(" ", "_")+""">.
                    ?p rdfs:label ?lbl.
                filter(langMatches(lang(?lbl),"EN"))
  
                }"""
        
        sparql.setQuery(prefixes+query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        for result in results["results"]["bindings"]:
            r.append([result["lbl"]["value"]])
    except :
        pass
    if len(r) < 1:
        r = ['0']
    return r

def exist_kb_pre(tuples,rel_type,endpoint=sparql,prefixes=prefixes):
    try:
        query = """
                ASK {
                 <http://dbpedia.org/resource/"""+tuples[0].replace(" ", "_") +"""> 
                ?p
                 <http://dbpedia.org/resource/"""+tuples[1].replace(" ", "_")+""">.
                    
  
                }"""
        sparql.setQuery(prefixes+query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        if results['boolean'] == False:
            return 0
        else:
            return 1
            
        
    except:
        pass

def exist_kb_recall(tuples,rel_type,endpoint=sparql,prefixes=prefixes):
    try:
        query = """
                ASK {
                 <http://dbpedia.org/resource/"""+tuples[0].replace(" ", "_") +"""> 
                 <http://dbpedia.org/ontology/"""+rel_type+""">
                 <http://dbpedia.org/resource/"""+tuples[1].replace(" ", "_")+""">.
                    
  
                }"""
        sparql.setQuery(prefixes+query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        if results['boolean'] == False:
            return 0
        else:
            return 1
            
        
    except:
        pass
