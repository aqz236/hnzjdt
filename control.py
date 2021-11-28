#coding=utf-8
from fuzzywuzzy import fuzz
import tool.driver as driver
import requests,json
info = {
    "题库": {},
    "学校信息": {}
}

#获取最新题库和学校信息
def getInfo():
    global tiku,schoolInfo
    tikuURL = 'https://blog-static.cnblogs.com/files/FSHOU/tikuData.js'
    schoolInfoURL = 'https://blog-static.cnblogs.com/files/FSHOU/schoolInfo.js'
    tikuInfo = json.loads(requests.get(tikuURL).text.replace("\'","\""))
    info["题库"] = tikuInfo["data"]
    print("题库获取完成 最近更新时间：",tikuInfo["updatetime"])
    schoolInfos = json.loads(requests.get(schoolInfoURL).text.replace("\'","\""))
    info["学校信息"] = schoolInfos["data"]
    print("学校信息获取完成, 最近更新时间：", schoolInfos["updatetime"])


def run(schoolName,userId,userPasswd):
    code = driver.login(userId,userPasswd,schoolName,info["题库"],info["学校信息"])
    return code

if __name__ == "__main__":
    getInfo()
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
            exit()
        elif code == 2:
            print("学校信息不存在，请手动添加学校学校或者联系作者")
        elif code == 3:
            print("登录有误，请尝试重新登录")
        else:
            pass


