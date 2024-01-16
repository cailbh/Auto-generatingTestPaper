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

inputDirO = r"" + fileName + "/ZhiShiDianO.json"
inputDir = "" + fileName + "/ProDelAddConGPT.json"
inputDir3 = "" + fileName + "/ZhiSHiDianEm.json"
outFile1 = r"" + fileName + "/problems_ConceptRel.json"
outFile2 = r"" + fileName + "/ZhiShiDian.json"
outFile3 = r"" + fileName + "/sankeyDataConO_ConGPTKM1.json"
i = 0
final_result = {}
result = []
edges = []
conOri = []
linkMapConO_ConGPT = {}
linkMapConO_Pro = {}
linkMapConGPT_ConGPTKM = {}

linkConO_ConGPT = []
linkConO_Pro = []
linkConGPT_ConGPTKM = []

conGPT = []
with open(inputDirO, "r", encoding="utf-8") as f:
    conOri = json.load(f)
    print(len(conOri))
with open(inputDir3, "r", encoding="utf-8") as f:
    conGPT = json.load(f)
    print(len(conOri))

with open(inputDir, "r", encoding="utf-8") as f:
    content = json.load(f)
    for problem in content:  # problems:
        i = i + 1
        knowledgePointPaths = problem['knowledgePointPaths']
        conOriList = []
        for kps in knowledgePointPaths:
            # print(kps)
            for kp in kps['knowledgePoints']:
                # print(kp)
                if (int(kp['id']) >= 64) & (int(kp['id']) <= 88):
                    temp = {
                        'conceptId': str(int(kp['id']) - 63),
                        'problemId': str(problem['id'])
                    }
                    conOriList.append(int(kp['id']) - 63)
                    edges.append([str("kp_" + kp['id']), str("pro_" + problem['id'])])
                    result.append(temp)
        for cG in problem['res']:
            cgD = conGPT[int(cG)]
            KLab = cgD['kLab']

            for cO in conOriList:
                linid1 = "kL" + str(KLab) + "_ch" + str(cG) + ""
                if linid1 in linkMapConGPT_ConGPTKM.keys():
                    linkMapConGPT_ConGPTKM[linid1] = linkMapConGPT_ConGPTKM[linid1] + 1
                else:
                    linkMapConGPT_ConGPTKM[linid1] = 1

                linid = "cO" + str(cO) + "_kL" + str(KLab) + ""
                if linid in linkMapConO_ConGPT.keys():
                    linkMapConO_ConGPT[linid] = linkMapConO_ConGPT[linid] + 1
                else:
                    linkMapConO_ConGPT[linid] = 1
    print(linkMapConO_ConGPT)
    lenGPTC = 0
    for t in linkMapConO_ConGPT:
        tsp = t.split("_")
        source = tsp[0][2:]
        target = tsp[1][2:]
        if lenGPTC < int(target) + len(conOri):
            lenGPTC = int(target) + len(conOri)
        linkTemp = {'source': int(source) - 1, 'target': int(target) + len(conOri), 'value': linkMapConO_ConGPT[t]}
        linkConO_ConGPT.append(linkTemp)
    for t in linkMapConGPT_ConGPTKM:
        print(t)
        tsp = t.split("_")
        source = tsp[0][2:]
        target = tsp[1][2:]
        linkTemp = {'source': int(source) + len(conOri), 'target': int(target) + lenGPTC + 1,
                    'value': linkMapConGPT_ConGPTKM[t]}
        linkConO_ConGPT.append(linkTemp)

with open(outFile2, "w", errors="igone", encoding="utf-8") as f:
    f.write(json.dumps(final_result, indent=4, ensure_ascii=False))

with open(outFile1, "w", errors="igone", encoding="utf-8") as f:
    f.write(json.dumps(result, indent=4, ensure_ascii=False))

with open(outFile3, "w", errors="igone", encoding="utf-8") as f:
    f.write(json.dumps(linkConO_ConGPT, indent=4, ensure_ascii=False))

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
