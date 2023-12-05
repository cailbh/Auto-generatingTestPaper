"""
coding:utf-8
@Software:PyCharm
@Time:2023/9/18 14:09
@Author:cailbh
@Introduce: 处理问题数据 知识点处理
"""
import json

inputDir = r"problemsDelZhiPu.json"
outFile1 = "problems_ConceptRel.json"
outFile2 = "ZhiShiDian.json"
i = 0
final_result = {}
result = []
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
                result.append(temp)

with open(outFile2, "w", errors="igone", encoding="utf-8") as f:
    f.write(json.dumps(final_result, indent=4, ensure_ascii=False))

with open(outFile1, "w", errors="igone", encoding="utf-8") as f:
    f.write(json.dumps(result, indent=4, ensure_ascii=False))
