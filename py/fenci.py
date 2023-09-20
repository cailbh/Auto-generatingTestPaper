"""
coding:utf-8
@Software:PyCharm
@Time:2023/9/19 11:50
@Author:cailbh
@Introduce: fenci

"""
import json
import re
import jieba
from collections import Counter

inputDir = r"problemsDelZhiPu.json"
outFile1 = "problemsDel_ZhiSHiDian.json"
outFile2 = "ZhiShiDian.json"
i = 0
final_result = {}


def clean_text(text):
    # 清洗文本数据
    cleaned_text = re.sub(r"[^u4e00-u9fa5]", "", text)
    return cleaned_text


def tokenize(text):
    # 分词
    tokens = jieba.lcut(text)
    return tokens


text = "这是一段需要清洗和分词的文本。"
cleaned_text = clean_text(text)
tokens = tokenize(cleaned_text)
print(tokens)


def build_vocabulary(tokens):
    # 构建词汇表
    word_counts = Counter(tokens)
    vocabulary = sorted(word_counts, key=word_counts.get, reverse=True)
    return vocabulary


import numpy as np


def generate_word_vectors(tokens, vocabulary):
    word_vectors = []
    for token in tokens:
        vector = [0] * len(vocabulary)
        if token in vocabulary:
            vector[vocabulary.index(token)] = 1
        word_vectors.append(vector)
    return np.array(word_vectors)


vocabulary = build_vocabulary(tokens)
print(vocabulary)

word_vectors = generate_word_vectors(tokens, vocabulary)
print(word_vectors)
# with open(inputDir, "r", encoding="utf-8") as f:
#     content = json.load(f)
#
# with open(outFile2, "w", errors="igone", encoding="utf-8") as f:
#     f.write(json.dumps(final_result, indent=4, ensure_ascii=False))
