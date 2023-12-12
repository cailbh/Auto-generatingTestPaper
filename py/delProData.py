"""
coding:utf-8
@Software:PyCharm
@Time:2023/9/14 17:09
@Author:cailbh
@Introduce: 处理问题数据 格式
"""
import json

inputDir = r"fs2.json"
outFile = "allProblemsDel.json"
i = 0
final_result = []
keys = ['id', "title", "content", "type", "difficulty", "score", "knowledgePointPaths","referenceCount"]
with open(inputDir, "r", encoding="utf-8") as f:
    content = json.load(f)
    # print(content)
    # problems = content['problems']
    for pro in content:  # problems:
        if 'problem' in pro:
            problem = pro['problem']
            ct = {"sortId": i}
            i = i + 1
            for key in keys:
                ct[key] = problem[key]

            final_result.append(ct)

with open(outFile, "w", errors="igone", encoding="utf-8") as f:
    f.write(json.dumps(final_result, indent=4, ensure_ascii=False))
