import json

import openai
import os
from IPython.display import display, Markdown, Latex
from langchain.llms import OpenAI
from dotenv import load_dotenv

from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

inputDir = r"problemsDel.json"
outFile = "problemsDelZhiPu.json"
result = []
# openai.api_key = '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'  # 3/min

openai.api_key = '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'  # 60/min
# openai.api_key = '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'

# system prompt，用于告诉GPT当前的情景，不了解可以放空，没有影响。
# system prompt例如：'You are a marketing consultant, please answer the client's questions in profession style.'
system_content = ''

# 这里使用了langchain包简化与GPT的对话过程，基于的是GPT-3.5，能力与免费版的chatGPT相同。GPT-4需要自行申请加入waitlist
messages = [SystemMessage(content=system_content)]

# 一轮最多对话20次，防止过长的对话。可以通过while循环条件修改。
i = 0
with open(inputDir, "r", encoding="utf-8") as f:
    content = json.load(f)
    # print(content)
    # problems = content['problems']
    for problem in content:  # problems:

        i = i + 1
        print(i)

        if i >= 59:
            chat = ChatOpenAI(temperature=0, openai_api_key=openai.api_key)
            resP = problem
            pContent = problem['content']
            print(problem['type'])
            pmt = "你现在是C语言程序设计任课教师，熟悉C语言程序设计这门课的知识点分布，请提取出下列c语言课程习题所涉及到的知识点，知识点来自于c语言课程，你的输出格式应当为json" \
                  "形式包含每个知识点的名称以及一段对该知识点进行教学的描述，输出的格式如[{'name':'...'，'description':'...'}],习题类型为：" + \
                  problem['type'] + ",题目具体内容为：'''" + pContent + "'''"

            messages=[(HumanMessage(content=pmt))]
            response = chat(messages)
            res = response.content

            problem['res'] = res
            result.append(problem)
            with open(outFile, "w", errors="igone", encoding="utf-8") as f:
                f.write(json.dumps(result, indent=4, ensure_ascii=False))
        # if i == 59:
        #     break


    # i = 1
    # while i <= 20:
    #     chat = ChatOpenAI(temperature=0, openai_api_key=openai.api_key)
    #
    #     user_input = input()
    #
    #     # 输入\end结束
    #     if user_input == '\end':
    #         break
    #     # 输入\clear清空当前对话重来，重置对话场景
    #     if user_input == '\clear':
    #         i = 1
    #         messages = [SystemMessage(content=system_content)]
    #         continue
    #
    #     messages.append(HumanMessage(content=user_input))
    #
    #     response = chat(messages)
    #     messages.append(AIMessage(content=response.content))  # 将GPT回复加入到对话
    #
    #     print("[GPT] Round " + str(i))
    #     print(response.content)
    #     display(Markdown(response.content))

    i = i + 1

print("\n --- END ---")
