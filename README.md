## 自动健康打卡程序
这是一个挂**服务器**上每天帮你定时健康打卡的程序

### 环境配置
该程序需要有python3环境
#### 1.安装chromedriver
```
sudo apt-get install chromium-chromedriver
```

#### 2.安装selenium库
```
pip install selenium
```

### 运行程序

#### 修改config.json配置文件
配置文件例如：
```
{
    "user": {   
        "username":"22021206" , 
        "schedule": {
            "hour": "10",
            "minute": "30"
        }
    }
}
```
`username`:填写你的学号  
`schedule`:填写每天打卡的定时时间  

### 启动程序
命令为
```
echo "xxx" | nohup python -u main.py > log.txt 2>&1 &
```
请将`xxx`改为你的密码。  
打卡的日志可以从`log.txt`中看到。
