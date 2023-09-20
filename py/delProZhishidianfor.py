"""
coding:utf-8
@Software:PyCharm
@Time:2023/9/18 14:09
@Author:cailbh
@Introduce: 处理问题数据 知识点处理
"""
import json

inputDir = r"problemsDelZhiPu.json"
outFile1 = "problemsDel_ZhiSHiDian.json"
outFile2 = "ZhiShiDian.json"
i = 0
final_result = {}
with open(inputDir, "r", encoding="utf-8") as f:
    content = json.load(f)
    for problem in content:  # problems:
        i = i + 1
        kps = problem['res'].replace('"', "'").replace("，", ',').replace("\\", " ").replace("{'", '{"').replace("': '",
                                                                                                                '": "').replace(
            "': '", '": "').replace("', '", '", "').replace("'}", '"}').replace("':'", '":"').replace("':'",
                                                                                                      '":"').replace(
            "','", '","').replace("'}", '"}')
        if kps[len(kps) - 1] != ']':
            kps += '"}]'
        print(kps)
        jsonKps = json.loads(kps)
        for kp in jsonKps:
            kpName = kp['name']
            if 'description' not in kp:
                continue
            if kpName in final_result.keys():
                final_result[kpName].append(kp['description'])
            else:
                final_result[kpName] = [kp['description']]

    print(len(final_result))
    for zsd in final_result:
        print(zsd, final_result)

with open(outFile2, "w", errors="igone", encoding="utf-8") as f:
    f.write(json.dumps(final_result, indent=4, ensure_ascii=False))
