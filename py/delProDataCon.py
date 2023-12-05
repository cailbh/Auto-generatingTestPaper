"""
coding:utf-8
@Software:PyCharm
@Time:2023/10/18 17:09
@Author:cailbh
@Introduce: 处理问题知识点数据 格式
"""
import json


def linear_searchByName(arr, name):
    for i in range(len(arr)):
        if arr[i]['name'] == name:
            return [i, arr[i]]
    return -1


inputDir = r"ZhiShiDian.json"
inputDirP = r"problemsDelZhiPu.json"
outFile = "ZhiShiDianS.json"
i = 0
final_result = {}
keys = ['id', "title", "content", "type", "difficulty", "score", "knowledgePointPaths"]
# with open(inputDir, "r", encoding="utf-8") as f:
#     content = json.load(f)
#     # print(content)
#     # problems = content['problems']
#     for zsd in content:  # problems:
#         ct = {"sortId": i}
#         i = i + 1
#         ct['name'] = zsd
#         ct['description'] = content[zsd]
#         # for key in keys:
#         #     ct[key] = problem[key]
#
#         final_result.append(ct)

with open(inputDirP, "r", encoding="utf-8") as fp:
    problems = json.load(fp)
    # print(content)
    # problems = content['problems']
    for pro in problems:  # problems:
        rels = pro['res']
        kps = pro['res'].replace('"', "'").replace("，", ',').replace("\\", " ").replace("{'", '{"').replace("': '",
                                                                                                            '": "').replace(
            "': '", '": "').replace("', '", '", "').replace("'}", '"}').replace("':'", '":"').replace("':'",
                                                                                                      '":"').replace(
            "','", '","').replace("'}", '"}')
        if kps[len(kps) - 1] != ']':
            kps += '"}]'
        jsonKps = json.loads(kps)
        for kp in jsonKps:
            print(kp)
            kpName = kp['name']
            if 'description' not in kp:
                continue
            if kpName in final_result.keys():
                final_result[kpName].append(kp['description'])
            else:
                # name.append(kpName)
                # zsdIdMap[kpName] = {"sortId": j}
                j = j + 1
                final_result[kpName] = [kp['description']]
            # for rel in rels:
            # zsd = linear_searchByName(final_result, kp['name'])
            # print(zsd)

with open(outFile, "w", errors="igone", encoding="utf-8") as f:
    f.write(json.dumps(final_result, indent=4, ensure_ascii=False))
