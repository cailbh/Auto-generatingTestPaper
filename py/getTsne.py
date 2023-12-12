"""
coding:utf-8
@Software:PyCharm
@Time:2023/12/15 14:09
@Author:cailbh
@Introduce: TSNE
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from sklearn.manifold import TSNE

from sklearn.cluster import KMeans, HDBSCAN

nn = "week"
mm = "dw"
outFileDur = 'problems_ConceptRel_vector_tsne'
fl = open("problems_ConceptRel_vector.txt")
dataMat = []
idMat = []

i = 0
for line in fl.readlines():
    if i == 0:
        i = i + 1
    else:
        i = i + 1
        curLine = line.strip().split(" ")
        idMat.append(curLine[0])
        del curLine[0]
        dataMat.append(curLine)

X = np.array(dataMat)  # [[12, 23, 3], [23, 45, 6], [4, 5, 7], [6, 3, 5]])
print(X)
X_tsne = TSNE(n_components=2, learning_rate=100).fit_transform(X)
f = open(outFileDur + ".txt", 'w')  # 若是'wb'就表示写二进制文件
f.write('id,x,y\n')
j = 0
tm = []
cluster = HDBSCAN(min_cluster_size=50).fit(X)
kmeans = KMeans(n_clusters=7, random_state=0).fit(X_tsne)
k_li = cluster.labels_
# kc_li = cluster.cluster_centers_.tolist()
# print(k_li, kc_li)
color = ['red', 'green', 'blue', 'cyan', 'magenta', 'yellow', 'black']
resultP = []

for i in idMat:
    f.write(i + ",")
    idm = i.split("_")
    type = idm[0]
    id = idm[0]
    f.write(str(X_tsne[j][0]) + "," + str(X_tsne[j][1]) + "\n")
    tm.append({"id": id, "kLab": str(k_li[j]), "type": type, "x": float(X_tsne[j][0]), "y": float(X_tsne[j][1])})
    j = j + 1
f.close()

k = 0
for point in X_tsne:
    # co = 'black'
    # if k_li[k] <= 6:
    co = color[k_li[k] % 7]
    plt.scatter(point[0], point[1], c=co)
    if k % 10 == 0:
        plt.text(point[0], point[1], idMat[k], fontsize=12)
    k = k + 1

plt.show()
# tm = {'50': {'x': -5.0395074, 'y': -8.343899}, '150': {'x': -3.7801764, 'y': 10.737326}}
with open(outFileDur + ".json", 'w') as fw:
    json.dump(tm, fw)

# print(X_embedded)
