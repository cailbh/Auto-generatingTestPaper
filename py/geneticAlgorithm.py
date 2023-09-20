"""
coding:utf-8
@Software:PyCharm
@Time:2023/9/13 11:24
@Author:cailbh
@Introduce: 遗传算法
"""
from random import random

pop_size = 5  # 种群数量
pop_size = 5  # 种群数量
max_value = 10  # 基因中允许出现的最大值
chrom_length = 10  # 染色体长度 题目数量
pc = 0.6  # 交配概率
pm = 0.01  # 变异概率
results = [[]]  # 存储每一代的最优解，N个二元组
fit_value = []  # 个体适应度
fit_mean = []  # 平均适应度


def geneEncoding(pop_size, chrom_length):
    pop = [[]]
    for i in range(pop_size):
        temp = []
        for j in range(chrom_length):
            temp.append(random.randint(0, 1))
        pop.append(temp)

    return pop[1:]


pop = geneEncoding(pop_size, chrom_length)
