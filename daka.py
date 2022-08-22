import time
import random
import functools
from datetime import datetime

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = None

url = 'https://healthreport.zju.edu.cn/ncov/wap/default/index'


question_choice = {
    'sfzx': '是 Yes', # 今日是否在校
    'campus': '玉泉校区 Yuquan ', # 所在校区
    'internship': '否 No', # 今日是否进行实习或实践

    'sqhzjkkys': '绿码 Green code', # 今日申领校区所在地健康码的颜色？
    'tw': '否 No', # 今日是否有发热症状（高于37.2 ℃）？
    'sfcxzysx': '否 No', # 今日是否有涉及涉疫情的管控措施
    'sfjcbh': '否 No', # 是否有与新冠疫情确诊人员或密接人员有接触的情况? 
}

location = {
    'long': 120.12445439312742,
    'lat': 30.26638054406842
}



def synchronize_trial(delay, max_trial=10, msg=''):
    def decorator_synchronize_trial(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            trials = 0
            while True:
                trials += 1
                if trials == max_trial:
                    raise NotImplementedError
                time.sleep(delay)
                try:
                    return func(*args, **kw)
                except BaseException as e:
                    print(e)
                    print(msg)
        return wrapper
    return decorator_synchronize_trial


@synchronize_trial(delay=0.5, msg='未找到用户名和密码输入框，正在重试')
def login(username, password):
    username_box = driver.find_element('id', 'username')
    username_box.send_keys(username)
    password_box = driver.find_element('id', 'password')
    password_box.send_keys(password)
    login_btn = driver.find_element('id', 'dl')
    login_btn.click()


@synchronize_trial(delay=0.5, msg='未找到对应选项，正在重试')
def fill_form():
    print('开始填选选项...')
    for div_name, choice in question_choice.items():
        div = driver.find_element('name', div_name)
        btn = div.find_element('xpath', f"./div/div/span[text()='{choice}']")
        btn.click()
        time.sleep(1)
    place_span = driver.find_element('name', 'area')
    place_span.click()
    time.sleep(1)
    # agree_div = driver.find_element('name', 'sfqrxxss')
    # agree_div.click()


def do_daka(username, password, delay=0):
    if delay > 0:
        time_delay = random.randint(1, delay)
        print(f'请等待{time_delay} s')
        time.sleep(time_delay)
        
    global driver
    driver = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)
    driver.execute_cdp_cmd(
        "Browser.grantPermissions",  # 授权地理位置信息
        {
            "origin": "https://healthreport.zju.edu.cn/",
            "permissions": ["geolocation"]
        },
    )
    driver.execute_cdp_cmd(
        "Emulation.setGeolocationOverride",  # 虚拟位置
        {
            "latitude": location['lat'],
            "longitude": location['long'],
            "accuracy": 50,
        },
    )
    print(driver)
    driver.get(url)
    print('开始登录...')
    login(username, password)
    print(f'登录成功，账号{username}')
    fill_form()
    print('表单填写完成，准备提交信息...')
    submit_btn = driver.find_element('xpath', "//*[contains(text(), '提交信息')]")
    submit_btn.click()
    time.sleep(2)
    comfirm_btn = driver.find_element('css selector', 'div.wapcf-btn.wapcf-btn-ok')
    comfirm_btn.click()
    print('打卡信息提交成功!!')

    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
    print(f'✅ 打卡成功，用户: {username}, 打卡时间: {dt_string}')


if __name__ == '__main__':
    do_daka('22021206', 'zju244712')
