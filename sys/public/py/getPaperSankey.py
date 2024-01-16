# print("py")
import sys
import geneticAlgorithm as gE
from pymongo import MongoClient

client = MongoClient('mongodb://127.0.0.1:27017')
my_col = client['ProData']['testProblem']

# datas = my_col.find({}, {'_id': 0, 'author': 0, 'owner': 0, 'status': 0, 'rejectReason': 0, 'updateAt': 0,
#                          'manageable': 0, 'compiler': 0, 'problemTags': 0, 'selfCheckStatus': 0,
#                          'selfCheckSubmissionId': 0, 'reviewerUserId': 0, 'authorOrganizationId': 0})
problems = my_col.find()


# for pro in problems:
#   print(pro)
#   my_col1.insert_one(data)

# gE.main(60, 300, 0.7, 0.05, -1.57, 20.18, 3)

# generation = gE.initializationPro(problems)

# population为种群；generations为进化代数，cross_probabilit为交叉概率
# mutation_probability为变异概率，[start,end]为定义域，precision为精度
def main(problemList, population, generations, problemLen, difficulty, cross_probability, mutation_probability, ):
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
    for t in best:
        temp = []
        for p in t:
            temp.append(problemList[p]['id'])
        result.append(temp)
    print(result)
    # print(round(best, precision), round(pow(best, 3) * math.cos(best), precision))


generation = problems
if __name__ == '__main__':
    # print([11,sys.argv[1]])
    problems = list(problems)
    main(problems, 60, 10, [sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]], 0.5, 0.7, 0.05)