"""
coding:utf-8
@Software:PyCharm
@Time:2023/9/18 14:09
@Author:cailbh
@Introduce: 处理问题数据 知识点处理
"""
import json
from node2vec import Node2Vec
import networkx as nx

inputDir = r"ZhiShiDianO.json"
inputDirO = r"problemsDelZhiPu.json"
outFile1 = "problems_ConceptRel.json"
outFile2 = "ZhiShiDian.json"
i = 0
final_result = {}
result = []
edges = []
with open(inputDir, "r", encoding="utf-8") as f:
    content = json.load(f)
    for problem in content:  # problems:
        i = i + 1
        knowledgePointPaths = problem['knowledgePointPaths']
        print(problem)
        for kps in knowledgePointPaths:
            # print(kps)
            for kp in kps['knowledgePoints']:
                print(kp)
                temp = {
                    'conceptId': str(kp['id']),
                    'problemId': str(problem['id'])
                }
                edges.append([str("kp_"+kp['id']), str("pro_"+problem['id'])])
                result.append(temp)

with open(outFile2, "w", errors="igone", encoding="utf-8") as f:
    f.write(json.dumps(final_result, indent=4, ensure_ascii=False))

with open(outFile1, "w", errors="igone", encoding="utf-8") as f:
    f.write(json.dumps(result, indent=4, ensure_ascii=False))

# FILES
EMBEDDING_FILENAME = "problems_ConceptRel_vector.txt"
EMBEDDING_MODEL_FILENAME = 'problems_ConceptRel_embeddings.model'
INPUTEDGE_FILENAME = "problems_ConceptRel.txt"


# Create a graph
graph = nx.Graph()
graph.add_edges_from(edges)

# Precompute probabilities and generate walks
node2vec = Node2Vec(graph, dimensions=128, walk_length=30, num_walks=200, workers=4)

## if d_graph is big enough to fit in the memory, pass temp_folder which has enough disk space
# Note: It will trigger "sharedmem" in Parallel, which will be slow on smaller graphs
# node2vec = Node2Vec(graph, dimensions=64, walk_length=30, num_walks=200, workers=4, temp_folder="/mnt/tmp_data")

# Embed
model = node2vec.fit(window=10, min_count=1,batch_words=4)  # Any keywords acceptable by gensim.Word2Vec can be
# passed, `diemnsions` and `workers` are automatically passed (from the Node2Vec constructor)

# Look for most similar nodes
model.wv.most_similar('2')  # Output node names are always strings

# Save embeddings for later use
model.wv.save_word2vec_format(EMBEDDING_FILENAME)

# Save model for later use
model.save(EMBEDDING_MODEL_FILENAME)