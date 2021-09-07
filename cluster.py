# -*- coding: utf-8 -*-

from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn import metrics

#num_clusters = 5
def cluster(corpus,embeddings,num_clusters=5):
    clustering_model = KMeans(n_clusters=num_clusters)
    clustering_model.fit(embeddings)
    labels = clustering_model.predict(embeddings)
    centroids  = clustering_model.cluster_centers_
    cluster_assignment = clustering_model.labels_
    centroid_labels = [centroids[i] for i in labels]
    
    #print("%.6f" % metrics.v_measure_score(centroid_labels, clustering_model.labels_))

    clustered_sentences = [[] for i in range(num_clusters)]
    for sentence_id, cluster_id in enumerate(cluster_assignment):
        clustered_sentences[cluster_id].append(corpus[sentence_id])
   
    return clustered_sentences
   
def cluster_HAC(corpus,embeddings,num_clusters = 5):
    cluster = AgglomerativeClustering(num_clusters, affinity='euclidean', linkage='ward')
    cluster.fit_predict(embeddings)
   
    
    cluster_assignment = cluster.labels_
    
    clustered_sentences = [[] for i in range(num_clusters)]
    for sentence_id,cluster_id in enumerate(cluster_assignment):
        clustered_sentences[cluster_id].append(corpus[sentence_id])
    return clustered_sentences
# =============================================================================
#     for i, cluster in enumerate(clustered_sentences):
#         print("Cluster ", i+1)
#         print(cluster)
#         for x in cluster:
#             for key, value in cand_sent.items(): 
#                 if x == value: 
#                     print(key) 
#     print("")
# =============================================================================
