#coding=utf-8
from fuzzywuzzy import fuzz
import tool.driver as driver
import requests,json,webbrowser
import os

info = {
    "题库": {},
    "学校信息": {},
    "最新消息":{}
}

#获取最新题库和学校信息
def getInfo():
    global tiku,schoolInfo
    tikuURL = 'https://blog-static.cnblogs.com/files/FSHOU/tikuData.js'
    schoolInfoURL = 'https://blog-static.cnblogs.com/files/FSHOU/schoolInfo2.js'
    tikuInfo = json.loads(requests.get(tikuURL).text.replace("\'","\""))
    info["题库"] = tikuInfo["data"]
    print("题库获取完成 最近更新时间：",tikuInfo["updatetime"])
    schoolInfos = json.loads(requests.get(schoolInfoURL).text.replace("\'","\""))
    info["学校信息"] = schoolInfos["data"]
    print("学校信息获取完成, 最近更新时间：", schoolInfos["updatetime"])
    info["最新消息"] = schoolInfos["msg"]
    print(info["最新消息"])
    info["update"] = schoolInfos["update"]
def run(schoolName,userId,userPasswd):
    code = driver.login(userId,userPasswd,schoolName,info["题库"],info["学校信息"])
    return code
def logo():
    print('''  ______   _                   
     |  ____| | |                  
     | |__ ___| |__   _____      __
     |  __/ __| '_ \ / _ \ \ /\ / /
     | |  \__ \ | | | (_) \ V  V / 
     |_|  |___/_| |_|\___/ \_/\_/  

                                   ''')
#主要函数
def main():

    while True:
        schoolName = input("请输入学校名称(Enter键入以下一步)：")
        if schoolName not in info["学校信息"]:
            print("学校信息不存在\n请尝试重新输入：\n【如果确认输入无误请自行修改源码添加学校或者联系作者】")
        else:
            userId = input("请输入学号(Enter键入以下一步)：")
            userPasswd = input("请输入密码(Enter键入以运行程序)：")
            code = run(schoolName,userId,userPasswd)
        code = 0
        if code == 1:
            print("执行完成")
        elif code == 2:
            print("学校信息不存在，请手动添加学校学校或者联系作者")
        elif code == 3:
            print("登录有误，请尝试重新登录")
        else:
            pass


def createHtml():
    try:
        os.remove(f'{userId}国家安全知识考试.html')
    except:
        pass
    with open(f'{userId}国家安全知识考试.html', 'a', encoding='utf-8')as f2:  # f2为文件描述符
        f2.write(htmlData)
    webbrowser.open(f'{userId}国家安全知识考试.html')
    time.sleep(2)
    os.remove(f'{userId}国家安全知识考试.html')
if __name__ == "__main__":
    version = 1.7
    print(f"当前版本：{str(version)}")
    logo()#打印logo
    getInfo()
    if info["update"]["latestVersion"] > version:
        print(f"当前程序版本v{str(version)}不是最新版本v",str(info["update"]["latestVersion"]))
        if info["update"]["level"] == 3:#更新等级 强制更新
            print("本次更新是重要更新，不更新将程序无法正常使用")
            print("更新内容：")
            print(info["update"]["updateMsg"])
            input("键入Enter跳转项目地址")
            webbrowser.open("https://github.com/aqz236/hnzjdt")
        else:
            print("本次更新非必要更新，下面是更新内容")
            print(info["update"]["updateMsg"])
            inputCode = input("输入1忽略更新，输入2跳转项目地址")
            if inputCode == 1 or inputCode == "1":
                main()
            elif inputCode == 2 or inputCode == "2":
                webbrowser.open("https://github.com/aqz236/hnzjdt")
    elif info["update"]["latestVersion"] == version:
        main()
    else:
        print("程序出错")
