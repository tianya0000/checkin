#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TG: https://t.me/+qWEhwrx8lCZiYTc1
cron: 1 7 * * *
new Env('阿里云盘签到');
变量 export refresh_token="refresh_token1&refresh_token2&refresh_token3"
"""


import json
import  requests
import os
from notify import send


filename='refresh_token.txt'

# 使用refresh_token更新access_token
def update_token(refresh_token):
    url = 'https://auth.aliyundrive.com/v2/account/token'
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    response = requests.post(url=url, json=data).json()
    access_token = response['access_token']
    refresh_token = response['refresh_token']
    nick_name = response['nick_name']
    print('更新refresh_token成功')
    return access_token,refresh_token,nick_name


#签到
def daily_check(access_token):
    url = 'https://member.aliyundrive.com/v1/activity/sign_in_list'
    headers = {
        'Authorization': access_token
    }
    response = requests.post(url=url, headers=headers, json={}).text
    result = json.loads(response)
    # print(result)
    if 'success' in result:
        print('签到成功')
        for i, j in enumerate(result['result']['signInLogs']):
            if j['status'] == 'miss':
                day_json = result['result']['signInLogs'][i-1]
                # print(day_json)
                if not day_json['isReward']:
                    content = '签到成功，今日未获得奖励'
                else:
                    content = '本月累计签到{}天,今日签到获得{}{}'.format(result['result']['signInCount'],
                                                                    day_json['reward']['name'],
                                                                    day_json['reward']['description'])
                print(content)
                return content


#更新refresh_token
def update_refsh_token(dict_refsh_tokens):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(json.dumps(dict_refsh_tokens))
        f.close()


#获取refresh_token
def get_refsh_token_Dict():
    refresh_token={}
    if os.path.exists(filename) == True:
        file = open(filename,'r')
        json_data = file.readline()
        print('从filename文件中读取的：'+json_data)
        refresh_token =json.loads(json_data)
    return refresh_token

def mian():
    print('更新access_token')
    refresh_tokens=os.environ["refresh_token"].split('&')
    dict_refsh_tokens = get_refsh_token_Dict()
    for refresh_token in refresh_tokens:
        try:
            ##从字典中获取上次更新的refresh_token
            dict_refsh_token = dict_refsh_tokens.get(refresh_token)
            temp_refresh_token = ''
            if dict_refsh_token != None:
                temp_refresh_token = dict_refsh_token
            else:
                temp_refresh_token = refresh_token
            access_token,new_refresh_token,nick_name = update_token(temp_refresh_token)
            if access_token !=None:
                print('更新access_token成功')
                # 将最新refresh_token存入字典中
                dict_refsh_tokens[refresh_token]=new_refresh_token
                content = daily_check(access_token)
                content_fist = 'TG讨论群：https://t.me/+qWEhwrx8lCZiYTc1 \n昵称：'+nick_name 
                send('阿里云盘签到', content_fist + content)  # 消息发送
        except Exception as e :
            print(e)
    #将字典写入文件中
    update_refsh_token(dict_refsh_tokens)

if __name__ == '__main__':
    mian()
