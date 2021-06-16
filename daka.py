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
    'sfyxjzxgym': '是 Yes', # 是否意向接种？
    'sfbyjzrq': '否', # 是否是不宜接种人群?
    'jzxgymqk': '已接种第一针', # 当前接种情况
    'sffrqjwdg': '否 No', # 今日是否因发热请假未到岗（教职工）或未返校（学生）？
    'sfqtyyqjwdg': '否 No', # 今日是否因发热外的其他原因请假未到岗（教职工）或未返校（学生）？
    'tw': '否 No', # 今日是否有发热症状（高于37.2 ℃）？
    'sfyqjzgc': '否 No', # 今日是否被当地管理部门要求在集中隔离点医学观察？
    'sfcyglq': '否 No', # 进入是否居家隔离观察
    'sfcxzysx': '否 No', # 是否有任何与疫情相关的，值得注意的情况？
    'sfsqhzjkk': '是 Yes', # 是否已经申领校区所在地健康码？
    'sqhzjkkys': '绿码 Green code', # 今日申领校区所在地健康码的颜色？
    'sfzx': '是 Yes', # 今日是否在校？
    'sfzgn': '境内 in Chinese Mainland', # 所在地点
    'sfymqjczrj': '否 No', # 本人家庭成员(包括其他密切接触人员)是否有近14日入境或近14日拟入境的情况？
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
    username_box = driver.find_element_by_id('username')
    username_box.send_keys(username)
    password_box = driver.find_element_by_id('password')
    password_box.send_keys(password)
    login_btn = driver.find_element_by_id('dl')
    login_btn.click()


@synchronize_trial(delay=0.5, msg='未找到对应选项，正在重试')
def fill_form():
    for div_name, choice in question_choice.items():
        div = driver.find_element_by_name(div_name)
        btn = div.find_element_by_xpath(f"./div/div/span[text()='{choice}']")
        btn.click()
        time.sleep(0.2)
    place_span = driver.find_element_by_name('area')
    place_span.click()
    time.sleep(1)
    agree_div = driver.find_element_by_name('sfqrxxss')
    agree_div.click()

def do_daka(username, password, delay=False):
    if delay:
        time_delay = random.randint(1, 1000)
        print(f'请等待{time_delay} s')
        time.sleep(time_delay)
        
    global driver
    driver = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)
    driver.get(url)
    print('开始登录...')
    login(username, password)
    print(f'登录成功，账号{username}')
    fill_form()
    print('表单填写完成，准备提交信息...')
    submit_btn = driver.find_element_by_xpath("//*[contains(text(), '提交信息')]")
    submit_btn.click()
    time.sleep(2)
    comfirm_btn = driver.find_element_by_css_selector('div.wapcf-btn.wapcf-btn-ok')
    comfirm_btn.click()
    print('打卡信息提交成功!!')

    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
    print(f'✅ 打卡成功，用户: {username}, 打卡时间: {dt_string}')

