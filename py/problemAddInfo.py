"""
coding:utf-8
@Software:PyCharm
@Time:2023/9/12 14:49
@Author:cailbh
@Introduce: 处理问题数据
"""
import json
import zhipuai

inputDir = r"problemsDel.json"
outFile = "problemsDelZhiPu.json"
i = 0
zhipuai.api_key = "e8c095a81c1040cf5e6071bc17cd378c.jCPoAEyNw1c3J4zp"
result = []
with open(inputDir, "r", encoding="utf-8") as f:
    content = json.load(f)
    # print(content)
    # problems = content['problems']
    for problem in content:  # problems:
        resP = problem
        i = i + 1
        print(i)
        pContent = problem['content']
        print(problem['type'])
        pmt = "你现在是C语言程序设计任课教师，熟悉C语言程序设计这门课的知识点分布，请提取出下列c语言课程习题所涉及到的知识点，知识点来自于c语言课程，你的输出格式应当为json" \
              "形式包含每个知识点的名称以及一段模仿教师对该知识点进行教学的描述，输出的格式如[{'name':'...'，'description':'...'}],习题类型为："+problem['type']+",题目具体内容为：'''"+pContent+"'''"

        response = zhipuai.model_api.sse_invoke(

            model="chatglm_6b",

            prompt=[{"role": "user", "content": pmt}],
            temperature=0.9,

            top_p=0.7,

            incremental=True

        )
        res = []
        for event in response.events():
            res.append(event.data)
        problem['res'] = res
        result.append(problem)
        if i == 1:
            break

with open(outFile, "w", errors="igone", encoding="utf-8") as f:
    f.write(json.dumps(result, indent=4, ensure_ascii=False))
# if __name__ == "__main__":
#
#     for event in response.events():
#
#         if event.event == "add":
#
#         elif event.event == "error" or event.event == "interrupted":
#             print("error")
#         elif event.event == "finish":
#             print("finish")
#         else:
#             print(event.data)
