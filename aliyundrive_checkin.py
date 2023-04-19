#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TG: https://t.me/+qWEhwrx8lCZiYTc1
cron: 1 7 * * *
new Env('阿里云盘签到');
变量 export refresh_token="xxxx"
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
    print('获取的access_token为：{}'.format(access_token))
    print('获取的refresh_token为：{}'.format(refresh_token))
    update_refsh_token(refresh_token)
    print('更新refresh_token成功')
    return access_token

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
def update_refsh_token(new_refresh_token):
    f = open(filename, "w")
    f.write(new_refresh_token)
    f.close()


#获取refresh_token
def get_refsh_token():
    refresh_token=None
    if os.path.exists(filename) == True:
        file = open(filename,'r')  #打开文件
        refresh_token = file.readline()
        print('从filename文件中读取的：'+refresh_token)

    if refresh_token == None:
        refresh_token=os.environ["refresh_token"]
    return refresh_token

def mian():
    print('更新access_token')
    refresh_token=get_refsh_token()
    access_token = update_token(refresh_token)
    print('更新成功，开始进行签到')
    content = daily_check(access_token)
    send('阿里云盘签到', content)  # 消息发送


if __name__ == '__main__':
    mian()
