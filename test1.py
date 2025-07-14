import openai
import os
import requests
import pandas as pd
import csv
from csv import DictWriter
from datetime import datetime

OPENAI_API_KEY="YOURAPIKEY"
openai.api_base = "https://vip.apiyi.com/v1"
openai.api_key = OPENAI_API_KEY

# Create OpenAI client
client = openai.OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=openai.api_base
)

# coding: utf-8

# openai.log = "debug"

#print(openai.Model.list())

DEBUG = False

#非流式响应
#completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello world!"}])
#print(completion.choices[0].message.content)

def gpt_api_stream(model, messages: list):
    """为提供的对话消息创建新的回答 (流式传输)

        gpt4长问题需要用流式传输，不然容易报错
    Args:
        messages (list): 完整的对话消息
        api_key (str): OpenAI API 密钥

    Returns:
        tuple: (results, error_desc)
    """
    try:
        response = client.chat.completions.create(
            #model='gpt-4',
            #model="gpt-3.5-turbo",
            model=model,
            messages=messages,
            stream=True,
            # temperature=0.5,
            # presence_penalty=0,

        )
        completion = {'role': '', 'content': ''}
        for event in response:
            if event.choices[0].finish_reason == 'stop':
                if DEBUG:
                    print(f'收到的完成数据: {completion}')
                break
            for delta_k, delta_v in event.choices[0].delta.dict().items():
                if delta_v is not None:  # Only add non-None values
                    if DEBUG:
                        print(f'流响应数据: {delta_k} = {delta_v}')
                    if delta_k == 'content':
                        completion['content'] += delta_v
                    elif delta_k == 'role':
                        completion['role'] = delta_v
        messages.append(completion)  # 直接在传入参数 messages 中追加消息
        msg = completion['content']     # 解析返回的msg
        return (True, msg, model)
    except Exception as err:
        return (False, f'OpenAI API 异常: {err}', model)

def gpt_api_no_stream(messages: list):
    

    try:
        completion = client.chat.completions.create(
            # model="gpt-3.5-turbo",
            # model="gpt-4",
            model="gpt-4-0613",
            messages=messages
        )
        # print(completion)
        
        msg = None
        choices = completion.choices
        if choices:
            msg = choices[0].message.content
        else:
            msg = completion.message.content
        return (True, msg)
    except Exception as err:
        return (False, f'OpenAI API 异常: {err}')


if __name__ == '__main__':
    ##Setting up everthing
    #print("avaliable_models",openai.Model.list())
    ## setting the model version
    model="gpt-3.5-turbo"
    is_code=False
    ##recording wheather the input is code data or not
    # 一次性回答版
    prompt = 'There are 9 birds in the tree, the hunter shoots one, how many birds are left in the tree？'  # 短问题
    #prompt="Please write a python code to solve bubble_sort problem. Lets take it step by step."
    # prompt = "鲁迅为什么暴打周树人"
    # prompt = "假如你是一个电力行业专家，请回答下面的问题：变压器有哪些部分组成"                                     # 长问题。可以把DEBUG变量设置为True来看流传输信息
    now = datetime.now()
 
    print("now =", now)
    



    print("发送：", prompt)
    print("使用的apikey：", openai.api_key)
    messages = [{'role': 'user','content': prompt},]
    
    ret, msg, model_recheck = gpt_api_stream(model,messages)
    # p, msg = gpt_api_no_stream(messages)
    print("返回：", msg)
    
    if DEBUG:
        print("messages：", messages)

    #column name   
    column_names =["input","output","model","is_code","time"]
    with open ("data.csv","a") as csvfile:
        
        #write a row
        dict_data={"input":prompt,"output":msg,"model":model_recheck,"is_code":is_code,"time":now}
        
        dictwriter_object = DictWriter(csvfile, fieldnames=column_names)
        dictwriter_object.writerow(dict_data)
        csvfile.close()
    

    
    # 问答版
    # messages = []
    # while True:
    #     prompt = input("Q: ")
    #     messages.append({'role': 'user','content': prompt})
    #     ret, msg = gpt_api_stream(messages)
    #     print("A：", msg)
