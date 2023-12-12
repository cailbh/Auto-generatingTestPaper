"""
coding:utf-8
@Software:PyCharm
@Time:2023/12/11 20:55
@Author:cailbh
@Introduce: hdbscan
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from sklearn.manifold import TSNE
import pandas as pd
from sklearn.cluster import HDBSCAN

nn = "week"
mm = "dw"
outFileDur = 'problems_ConceptGPT_HDBscan'
inputDir = 'ZhiSHiDianEm.json'
dataMat = []
idMat = []
with open(inputDir, "r", encoding="utf-8") as f:
    content = json.load(f)
    for con in content:  # problems:
        idMat.append(con['name'])
        dataMat.append([con['name']])
        # dataMat.append([con['x'], con['y']])
        # dataMat.append((con['name'],[con['x'], con['y']]))

# X = np.array(dataMat)  # [[12, 23, 3], [23, 45, 6], [4, 5, 7], [6, 3, 5]])
# print(X)
X = pd.DataFrame(np.random.rand(100, 10), columns=[f'V{i}' for i in range(10)])
print(X)
hdbscan = HDBSCAN().fit(X)
k_li = hdbscan.labels_
kc_li = hdbscan.feature_names_in_
print(k_li, kc_li)
# for k in k_li:
#     print(k)
# print(kc_li)
# with open(outFileDur + ".json", 'w') as fw:
#     json.dump(tm, fw)

# print(X_embedded)
