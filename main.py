from lib2to3.pytree import Base
import os
import json
import time
import datetime

import requests

from daka import do_daka


def send_message(msg):
    if not os.path.exists('./config.json'):
        return 
    configs = json.loads(open('./config.json', 'r').read())
    url = configs['message']['webhook']
    data = {
        'msg_type': 'text',
        'content': {
            'text': msg
        }
    }
    r = requests.post(url, json=data)
    assert r.code == 200


def daka(username, password):
    try:
        do_daka(username, password)
    except BaseException as e:
        print(e)
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
        send_message(f'[{dt_string}] 打卡失败，请检查\n错误内容: {e}')



def block_schedule(func, args, hour, minute):
    now = datetime.datetime.now()
    dt = datetime.datetime(now.year, now.month, now.day, int(hour), int(minute))
    next_time = int(dt.timestamp())
    now = int(time.time())
    while next_time - now < 0:
        dt += datetime.timedelta(days=1)
        next_time = int(dt.timestamp())
    
    while True:
        print(f'下一次定时启动时间: {dt}')
        time.sleep(next_time - now)
        func(*args)
        dt += datetime.timedelta(days=1)
        next_time = int(dt.timestamp())
        now = int(time.time())


def main():
    
    if os.path.exists('./config.json'):
        configs = json.loads(open('./config.json', 'r').read())
        user = configs["user"]
    else:
        print('Error: 请提供config.json文件')
        
    password = input('请输入密码:')
    
    print('⏰ 已启动定时程序，每天 %02d:%02d 为 %s 打卡' %(int(user["schedule"]["hour"]), int(user["schedule"]["minute"]),user["username"]))
    block_schedule(daka, 
                   args=[user["username"], password],
                   hour=user["schedule"]["hour"], minute=user["schedule"]["minute"])
    
    
if __name__ == "__main__":
    main()

