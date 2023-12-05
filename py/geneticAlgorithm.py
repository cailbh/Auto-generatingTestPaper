"""
coding:utf-8
@Software:PyCharm
@Time:2023/9/13 11:24
@Author:cailbh
@Introduce: 遗传算法
"""
import copy
import math
import random
import numpy as np

proType = [['MULTIPLE_CHOICE'], ['FILL_IN_THE_BLANK'], ['PROGRAMMING'], ['CODE_COMPLETION']]


# [start,end]为取值范围，precision为精度，即小数点后的位数
def get_binary_bit(start, end, precision):
    numbers = (end - start) * pow(10, precision) + 1
    if int(math.log(numbers, 2)) == math.log(numbers, 2):
        return int(math.log(numbers, 2))
    else:
        return int(math.log(numbers, 2)) + 1


# decimal为未编码的十进制数
def binary_encode(decimal, start, end, precision):
    bit = get_binary_bit(start, end, precision)
    # 将十进制数转为对应的二进制编码
    binary = bin(int((decimal - start) * pow(10, precision)))
    # 由于bin()生成的是0bxxxxx的形式，因此切片
    binary = str(binary)[2:]
    # 补齐位数
    while len(binary) < bit:
        binary = '0' + binary
    # 返回二进制编码
    return binary


# binary为二进制编码
def binary_decode(binary, start, precision):
    # 将二进制编码转为标准形式0bxxxxx
    binary = '0b' + binary
    # 将二进制编码转为十进制编码
    decimal = int(binary, 2)
    # 将十进制编码转为对应的十进制数
    decimal = start + decimal / pow(10, precision)
    return decimal


# population为种群大小
def initialization(population, start, end, precision):
    initialized = []
    for i in range(population):
        # 随机生成指定范围和精度的小数，并转为二进制编码
        random_float = random.uniform(start, end)
        random_float_precision = round(random_float, precision)
        random_binary = binary_encode(random_float_precision, start, end, precision)
        initialized.append(random_binary)
    # 返回初始化种群
    return initialized


# [optimize_start, optimize_end]为大致的估计区间
def initialization(population, start, end, precision, optimize_start, optimize_end):
    initialized = []
    for i in range(population):
        random_float = random.uniform(optimize_start, optimize_end)
        random_float_precision = round(random_float, precision)
        random_binary = binary_encode(random_float_precision, start, end, precision)
        initialized.append(random_binary)
    return initialized


def initializationPro(problems, population, problemLen, difficulty):
    initialized = []
    problemsInTypes = []
    problemsTemp = []
    for t in range(len(problemLen)):
        problemsInTypes.append([])
        problemsTemp.append([])
    for p in range(len(problems)):
        pType = problems[p]['type']
        for t in range(len(problemLen)):
            if pType in proType[t]:
                problemsInTypes[t].append(p)
    for i in range(population):
        temp = copy.deepcopy(problemsTemp)
        for t in range(len(problemLen)):
            ptLen = len(problemsInTypes[t])
            indexs = np.random.choice(list(range(ptLen)), size=problemLen[t])
            for index in indexs:
                temp[t].append(problemsInTypes[t][index])
        initialized.append(temp)
    return initialized


def fitness(binary, problemList, start, precision):
    # decimal = binary_decode(binary, start, precision)
    # fit = 1 / (pow(decimal, 3) * math.cos(decimal) + 4500)
    fit = 0
    for t in binary:
        for b in t:
            problem = problemList[b]
            fit = fit + (problem['difficulty'] + problem['score'])
    fit = 1 / fit
    return fit


# generation为该代待选择的种群
def select(generation, problemList, population, start, precision):
    # 计算所有个体的适应度
    all_fitness = []
    for binary in generation:
        fit = fitness(binary, problemList, start, precision)
        all_fitness.append(fit)
    fitness_array = np.array(all_fitness)
    # # 将适应度归一化，作为概率进行选择
    fitness_array = fitness_array / fitness_array.sum()
    selected_index = np.random.choice(list(range(population)), size=population, p=fitness_array)
    selected_index = selected_index.tolist()
    # # 将选择到的个体加入选择后的种群
    selected = []
    for index in selected_index:
        selected.append(generation[index])
    # 返回被选择之后的种群
    return selected


def in_range(binary, start, end, precision):
    if start <= binary_decode(binary, start, precision) <= end:
        return True
    else:
        return False


# selected为被选择之后的种群，probability为交叉概率
def cross(selected, population, probability, start, end, precision):
    # print(11111,len(selected[0]))
    crossed = selected[:]
    # bit = get_binary_bit(start, end, precision)
    # numbers为进行交叉的次数
    numbers = population * probability
    count = 0
    i = 0
    for t in range(len(selected[0])):
        while i < population - 1 and count < numbers:
            # 随机选取分割点
            position = random.randrange(1, len(crossed))
            # 将两个父二进制编码分别截成两个部分
            binary11 = selected[i][t][:position]
            binary12 = selected[i][t][position:]
            binary21 = selected[i + 1][t][:position]
            binary22 = selected[i + 1][t][position:]
            # # 将二进制编码切片重组形成新的两个子二进制编码
            binary1 = binary11 + binary22
            binary2 = binary21 + binary12
            crossed[i][t] = binary1
            crossed[i + 1][t] = binary2
            count += 1
            i += 2

    # print(111,crossed)
    # print(selected)
    # 返回交叉之后的种群
    return crossed


def reverse(string, position):
    string = list(string)
    if string[position] == '0':
        string[position] = '1'
    else:
        string[position] = '0'
    return ''.join(string)


# crossed为交叉之后的种群，probability为变异的概率
def mutation(crossed, population, probability, start, end, precision):
    mutated = crossed[:]
    bit = get_binary_bit(start, end, precision)
    for i in range(population):
        # 随机生成一个0-1之间的数，判断该二进制编码是否突变
        whether_mutated = True if random.random() < probability else False
        if whether_mutated:
            # 随机生成一个变异位，将该位进行取反
            position = random.randrange(0, bit)
            mutated_binary = reverse(crossed[i], position)
            # 若生成的新二进制编码不在定义域内，则重复生成直至符合条件
            while not in_range(mutated_binary, start, end, precision):
                position = random.randrange(0, bit)
                mutated_binary = reverse(crossed[i], position)
            mutated[i] = mutated_binary
    # 返回变异后的种群
    return mutated


# final_generation为最后一代种群
def search(final_generation, problemList, start, precision):
    # 计算所有个体的适应度，找到适应度最高的个体
    all_fitness = []
    for binary in final_generation:
        fit = fitness(binary, problemList, start, precision)
        all_fitness.append(fit)

    fitness_array = np.array(all_fitness)

    index = all_fitness.index(max(all_fitness))
    # 解码，返回最优解
    return final_generation[index]


# population为种群大小；generations为进化代数，cross_probabilit为交叉概率
# mutation_probability为变异概率，[start,end]为定义域，precision为精度
def main(population, generations, cross_probability, mutation_probability, start, end, precision):
    # 确定初始化种群（如图所示大致区间为[15,17]
    generation = initialization(population, start, end, precision, 15, 17)
    print(generation)
    for i in range(generations):
        # 选择
        generation = select(generation, population, start, precision)
        # 交叉
        generation = cross(generation, population, cross_probability, start, end, precision)
        # 变异
        generation = mutation(generation, population, mutation_probability, start, end, precision)
    # 搜索最优解，打印结果
    best = search(generation, start, precision)
    print(round(best, precision), round(pow(best, 3) * math.cos(best), precision))

# def geneEncoding(pop_size, chrom_length):
#     pop = [[]]
#     for i in range(pop_size):
#         temp = []
#         for j in range(chrom_length):
#             temp.append(random.randint(0, 1))
#         pop.append(temp)
#
#     return pop[1:]


# pop = geneEncoding(pop_size, chrom_length)
