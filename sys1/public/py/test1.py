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

result = []
# openai.api_key = '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'  # 3/min

openai.api_key = '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'  # 60/min

# system prompt，用于告诉GPT当前的情景，不了解可以放空，没有影响。
# system prompt例如：'You are a marketing consultant, please answer the client's questions in profession style.'
system_content = ''

# 这里使用了langchain包简化与GPT的对话过程，基于的是GPT-3.5，能力与免费版的chatGPT相同。GPT-4需要自行申请加入waitlist
messages = [SystemMessage(content=system_content)]

# 一轮最多对话20次，防止过长的对话。可以通过while循环条件修改。
i = 0
problem = {
    "sortId": 0,
    "id": "1701115978840051712",
    "title": "C01-04输入一个矩形的长和宽，求出周长及面积，并将结果小数点后保留2位输出。(20分)",
    "content": "输入一个矩形的长和宽，求出周长及面积，并将结果小数点后保留2位输出。\n\n### 输入格式:\n\n在用scanf函数输入数据之前，要输出如下提示性语句：\n\n```\n请依次输入长和宽:\n```\n\n### 输出格式:\n\n### 输入样例:\n\n在这里给出一组输入。例如：\n\n```in\n1.25 2.25\n```\n\n### 输出样例:\n\n在这里给出相应的输出。例如：\n\n```out\n请依次输入长和宽:\nlength=7.00,area=2.81\n```",
    "type": "PROGRAMMING",
    "difficulty": 1,
    "score": 20
}
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
print(res)


print("\n --- END ---")
