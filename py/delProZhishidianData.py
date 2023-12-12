"""
coding:utf-8
@Software:PyCharm
@Time:2023/9/18 14:09
@Author:cailbh
@Introduce: 处理问题数据 知识点处理 word2vec
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
from sklearn.cluster import KMeans,HDBSCAN
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AffinityPropagation

from pylab import *
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

model = Word2Vec("w2v-light-tencent-chinese")
inputDir = r"problemsDelZhiPu.json"
inputDirO = r"ZhiShiDianO.json"
outFile1 = "ZhiSHiDianEm.json"
outFile2 = "ZhiShiDian.json"
outFile3 = "ProConGPTRel.json"
stopwords_path = "stopwords.txt"
i = 0
j = 0
final_result = {}
zsdIdMap = {}

stopwords = []
# jieba.enable_paddle()
try:
    stopwords = open(stopwords_path, encoding='utf-8')
except:
    stopwords = []
    print("error in stop_file")


# 判断是否是中文
def is_chinese(strings):
    for _char in strings:
        if '\u4e00' <= _char <= '\u9fa5':
            return True


# 定义分词函数
def tokenizer(s):
    # jieba.load_userdict(dict_path)
    jieba.initialize()
    words = []
    cut = psg.cut(s)

    flag_list = ['n', 'nz', 'vn', 'nr', 'an', 'ns', 'i', 'nt', 'nz', ]
    for se_word in cut:
        word = re.sub(u'[^\u4e00-\u9fa5]', '', se_word.word)
        find = 0
        if word not in stopwords:
            if len(word) > 1:
                if find == 0 and se_word.flag in flag_list:
                    words.append(word)
    return words


name = []
dataMap = []
kpOri = []
result_rel = []
with open(inputDirO, "r", encoding="utf-8") as f:
    content = json.load(f)
    kpOri = content

with open(inputDir, "r", encoding="utf-8") as f:
    content = json.load(f)
    for problem in content:  # problems:
        i = i + 1
        kps = problem['res'].replace('"', "'").replace("，", ',').replace("\\", " ").replace("{'", '{"').replace("': '",
                                                                                                                '": "').replace(
            "': '", '": "').replace("', '", '", "').replace("'}", '"}').replace("':'", '":"').replace("':'",
                                                                                                      '":"').replace(
            "','", '","').replace("'}", '"}')
        if kps[len(kps) - 1] != ']':
            kps += '"}]'
        jsonKps = json.loads(kps)
        for kp in jsonKps:
            kpName = kp['name']
            temp = {}
            if 'description' not in kp:
                continue
            if kpName in final_result.keys():
                final_result[kpName].append(kp['description'])

                temp = {
                    'conceptId': str(zsdIdMap[kpName]['sortId']),
                    'problemId': str(problem['id'])
                }
            else:
                name.append(kpName)
                zsdIdMap[kpName] = {"sortId": j, "type": "normal"}
                temp = {
                    'conceptId': str(j),
                    'problemId': str(problem['id'])
                }
                j = j + 1
                final_result[kpName] = [kp['description']]
            result_rel.append(temp)
        for kp in kpOri:
            kpName = kp['name']
            if kpName in final_result.keys():
                final_result[kpName].append(kp['description'])
            else:
                name.append(kpName)
                zsdIdMap[kpName] = {"sortId": j, "type": "ori"}
                j = j + 1
                final_result[kpName] = [kp['description']]

    for zsd in final_result:
        strs = ""
        for st in final_result[zsd]:
            strs += st
        words = []
        if is_chinese(zsd):
            words = tokenizer(strs)
        else:
            words = strs.strip()
        if len(words) == 0:
            words = zsd
        embeddings = []
        sum_vector = []
        v = 0
        for word in words:
            wordEmbeddings = model.encode(word)
            if v == 0:
                sum_vector = wordEmbeddings
                v = v + 1
            else:
                sum_vector = [sum_vector[k] + wordEmbeddings[k] for k in range(len(wordEmbeddings))]
                v = v + 1
        embeddings = [sum_vector[k] / v for k in range(len(sum_vector))]
        if len(sum_vector) == 0:
            print(words, zsd)
        zsdIdMap[zsd]['embeddings'] = embeddings
        # print(embeddings)
        dataMap.append(embeddings)
    X = np.array(dataMap)
    X_tn = TSNE(n_components=2).fit_transform(X)

    print(X_tn)

k = 0
mpl.rcParams['font.sans-serif'] = ['SimHei']

kmeans = KMeans(n_clusters=7, random_state=0).fit(X_tn)

cluster = HDBSCAN(min_cluster_size=50).fit(X)
k_li = cluster.labels_
# kc_li = kmeans.cluster_centers_.tolist()
# print(k_li, kc_li)
color = ['red', 'green', 'blue', 'cyan', 'magenta', 'yellow']
resultP = []
for point in X_tn:
    plt.scatter(point[0], point[1], c=color[k_li[k]%6])
    temp = {}
    temp['x'] = float(np.float32(point[0]))
    temp['y'] = float(np.float32(point[1]))
    temp['kLab'] = str(k_li[k])
    temp['id'] = str(k)
    temp['name'] = str(name[k])
    resultP.append(temp)
    # if k % 10 == 0:
    #     plt.text(point[0], point[1], name[k], fontsize=12)
    k = k + 1

plt.show()
with open(outFile2, "w", errors="ignore", encoding="utf-8") as f:
    f.write(json.dumps(final_result, indent=4, ensure_ascii=False))

with open(outFile1, "w", errors="ignore", encoding="utf-8") as f:
    # f.write(json.dumps(zsdIdMap, indent=4, ensure_ascii=False))
    f.write(json.dumps(np.array(resultP).tolist(), indent=4, ensure_ascii=False))

with open(outFile3, "w", errors="ignore", encoding="utf-8") as f:
    f.write(json.dumps(result_rel, indent=4, ensure_ascii=False))
