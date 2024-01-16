"""
coding:utf-8
@Software:PyCharm
@Time:2023/10/31 11:24
@Author:cailbh
@Introduce: 自动组卷
"""

# print("py")
import sys
import geneticAlgorithm as gE
from pymongo import MongoClient

client = MongoClient('mongodb://127.0.0.1:27017')
my_col = client['ProData']['testProblem']
my_col1 = client['ProData']['conceptGptScatter']
my_conOri = client['ProData']['conceptOri']
paperSankeyData_col = client['ProData']['paperSankeyData']

# datas = my_col.find({}, {'_id': 0, 'author': 0, 'owner': 0, 'status': 0, 'rejectReason': 0, 'updateAt': 0,
#                          'manageable': 0, 'compiler': 0, 'problemTags': 0, 'selfCheckStatus': 0,
#                          'selfCheckSubmissionId': 0, 'reviewerUserId': 0, 'authorOrganizationId': 0})
problems = my_col.find()
conGPT = my_col1.find()

conOri = my_conOri.find()


def getsankeyData(problemList, paperId):
    edges = []
    linkMapConO_ConGPT = {}
    linkMapConO_Pro = {}
    linkMapConGPT_ConGPTKM = {}

    linkConO_ConGPT = []
    linkConO_Pro = []
    linkConGPT_ConGPTKM = []
    for problem in problemList:  # problems:
        knowledgePointPaths = problem['knowledgePointPaths']
        conOriList = []
        for kps in knowledgePointPaths:
            # print(kps)
            for kp in kps['knowledgePoints']:
                # print(kp)
                if (int(kp['id']) >= 64) & (int(kp['id']) <= 88):
                    edges.append([str("kp_" + kp['id']), str("pro_" + problem['id'])])
                    conOriList.append(int(kp['id']) - 63)
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
        tsp = t.split("_")
        source = tsp[0][2:]
        target = tsp[1][2:]
        linkTemp = {'source': int(source) + len(conOri), 'target': int(target) + lenGPTC + 1,
                    'value': linkMapConGPT_ConGPTKM[t]}
        linkConO_ConGPT.append(linkTemp)
    sankeyData = {
        "id": paperId,
        "link": linkConO_ConGPT
    }

    paperSankeyData_col.insert_one(sankeyData)


# for pro in problems:
#   print(pro)
#   my_col1.insert_one(data)

# gE.main(60, 300, 0.7, 0.05, -1.57, 20.18, 3)

# generation = gE.initializationPro(problems)

# population为种群；generations为进化代数，cross_probabilit为交叉概率
# mutation_probability为变异概率，[start,end]为定义域，precision为精度
def main(problemList, population, generations, problemLen, difficulty, cross_probability, mutation_probability,
         paperId):
    # 确定初始化种群（如图所示大致区间为[15,17]
    gloup = gE.initializationPro(problemList, population, problemLen, difficulty)
    for i in range(generations):
        # 选择
        gloup = gE.select(gloup, problemList, population, 0, 1)
        # 交叉
        gloup = gE.cross(gloup, population, cross_probability, 0, 0, 0)
        # print(gloup)
    #     # 变异
    #     gloup = mutation(gloup, population, mutation_probability, start, end, precision)
    # # 搜索最优解，打印结果
    best = gE.search(gloup, problemList, 0, 0)
    # print(str(best))
    result = []
    proList = []
    for t in best:
        temp = []
        for p in t:
            temp.append(problemList[p]['id'])
            proList.append(problemList[p])
        result.append(temp)
    print(result)
    getsankeyData(proList, paperId)
    # print(round(best, precision), round(pow(best, 3) * math.cos(best), precision))


generation = problems
if __name__ == '__main__':
    problems = list(problems)
    main(problems, 60, 10, [5, 0, 10, 0], 0.5, 0.7, 0.05, 0)
