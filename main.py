import os
import json
import time
import datetime

from daka import do_daka


def daka(username, password, delay):
    do_daka(username, password)


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
                   args=[user["username"], password, user["delay"]],
                   hour=user["schedule"]["hour"], minute=user["schedule"]["minute"])
    
    
if __name__ == "__main__":
    main()

