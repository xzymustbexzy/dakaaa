from lib2to3.pytree import Base
import os
import json
import time
import datetime
import random

import requests

from daka import do_daka


def send_message(msg):
    config = json.loads(open('./config.json', 'r').read())
    if 'message' not in config:
        return
    url = config['message']['webhook']
    data = {
        'msg_type': 'text',
        'content': {
            'text': msg
        }
    }
    r = requests.post(url, json=data)
    assert r.code == 200


def daka(username, password, delay):
    try:
        do_daka(username, password, delay)
    except BaseException as e:
        print(e)
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
        send_message(f'[{dt_string}] 打卡失败，请检查\n错误内容: {e}')



def block_schedule(func, args, hour, minute, random_delay_minute):
    delay_seconds = random_delay_minute * 60
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
        func(*args, delay=delay_seconds)
        dt += datetime.timedelta(days=1)
        next_time = int(dt.timestamp())
        now = int(time.time())


def main():
    
    if os.path.exists('./config.json'):
        config = json.loads(open('./config.json', 'r').read())
    else:
        print('Error: 请提供config.json文件')
    assert 'username' in config, '请在config.json文件中配置用户名'
    assert 'schedule' in config, '请在config.json文件中配置打卡时间'
        
    password = input('请输入密码:')
    
    print('⏰ 已启动定时程序，每天 %02d:%02d 为 %s 打卡' %(int(config['schedule']['hour']), int(config['schedule']['minute']), config["username"]))
    
    random_delay_minute = 0
    if 'random_delay_minute' in config['schedule']:
        random_delay_minute = config['schedule']['random_delay_minute']
    block_schedule(daka, 
                   args=[config['username'], password],
                   hour=config['schedule']['hour'], minute=config['schedule']['minute'],
                   random_delay_minute=random_delay_minute)

    
if __name__ == "__main__":
    main()

