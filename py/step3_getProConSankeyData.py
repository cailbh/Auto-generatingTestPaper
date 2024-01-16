"""
coding:utf-8
@Software:PyCharm
@Time:2023/12/12 18:59
@Author:cailbh
@Introduce:
"""
import json
import jieba

from text2vec import Word2Vec
import re
import jieba.posseg as psg

import numpy as np
# from cname import color
import pandas as pd
from sklearn.manifold import TSNE
import nltk
from nltk.tokenize import word_tokenize
from sklearn.manifold import SpectralEmbedding
from sklearn.cluster import KMeans, HDBSCAN
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AffinityPropagation

from pylab import *
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

fileName = 'pro1'

inputDir = r"" + fileName + "/ZhiShiDianO.json"
inputDirO = r"" + fileName + "/problemsDelKD.json"
outFile1 = r"" + fileName + "/problems_ConceptRel.json"
outFile2 = r"" + fileName + "/ZhiShiDian.json"
i = 0
final_result = {}
result = []
edges = []
with open(inputDirO, "r", encoding="utf-8") as f:
    content = json.load(f)
    for problem in content:  # problems:
        i = i + 1
        knowledgePointPaths = problem['knowledgePointPaths']
        print(problem)
        for kps in knowledgePointPaths:
            # print(kps)
            for kp in kps['knowledgePoints']:
                print(kp)
                if int(kp['id']) >= 64:
                    temp = {
                        'conceptId': str(int(kp['id']) - 63),
                        'problemId': str(problem['id'])
                    }
                    edges.append([str("kp_" + kp['id']), str("pro_" + problem['id'])])
                    result.append(temp)

with open(outFile2, "w", errors="igone", encoding="utf-8") as f:
    f.write(json.dumps(final_result, indent=4, ensure_ascii=False))

with open(outFile1, "w", errors="igone", encoding="utf-8") as f:
    f.write(json.dumps(result, indent=4, ensure_ascii=False))
#
# # FILES
# EMBEDDING_FILENAME = "problems_ConceptRel_vector.txt"
# EMBEDDING_MODEL_FILENAME = 'problems_ConceptRel_embeddings.model'
# INPUTEDGE_FILENAME = "problems_ConceptRel.txt"
#
#
# # Create a graph
# graph = nx.Graph()
# graph.add_edges_from(edges)
#
# # Precompute probabilities and generate walks
# node2vec = Node2Vec(graph, dimensions=128, walk_length=30, num_walks=200, workers=4)
#
# ## if d_graph is big enough to fit in the memory, pass temp_folder which has enough disk space
# # Note: It will trigger "sharedmem" in Parallel, which will be slow on smaller graphs
# # node2vec = Node2Vec(graph, dimensions=64, walk_length=30, num_walks=200, workers=4, temp_folder="/mnt/tmp_data")
#
# # Embed
# model = node2vec.fit(window=10, min_count=1,batch_words=4)  # Any keywords acceptable by gensim.Word2Vec can be
# # passed, `diemnsions` and `workers` are automatically passed (from the Node2Vec constructor)
#
# # Look for most similar nodes
# model.wv.most_similar('2')  # Output node names are always strings
#
# # Save embeddings for later use
# model.wv.save_word2vec_format(EMBEDDING_FILENAME)
#
# # Save model for later use
# model.save(EMBEDDING_MODEL_FILENAME)
