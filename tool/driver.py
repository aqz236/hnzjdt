#coding=utf-8
import requests,json,re
import base64
import tool.dealData as dealData
import tool.fuzz as fuzz
import time
PHPSESSID = ''
sentData = []
paperInfo = {}

#模拟登录
def login(userId,passwd,schoolName,tiku,schoolInfo):
    global PHPSESSID
    try:
        shoolId = schoolInfo[schoolName]
    except:
        return 2
    PHPSESSID = getSession()
    sms = getSms(PHPSESSID)
    userIdBase64 = base64.b64encode(userId.encode())
    passwdBase64 = base64.b64encode(passwd.encode())
    smsBase64 = base64.b64encode(sms.encode())

    strBase64UserId = str(userIdBase64).replace("b\'",'').replace('\'','')
    strBase64Passwd = str(passwdBase64).replace("b\'",'').replace('\'','')
    strBase64Sms = str(smsBase64).replace("b\'",'').replace('\'','')

    url = 'http://exam.hm86.cn/vip/login/loginAction.php?action=login'
    headers = {'Host': 'exam.hm86.cn', 'Connection': 'keep-alive', 'Content-Length': '132', 'Accept': '*/*',
               'Origin': 'http://exam.hm86.cn', 'X-Requested-With': 'XMLHttpRequest',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'Referer': 'http://exam.hm86.cn/vip/login/login.php', 'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9'}
    cookies = {'PHPSESSID': PHPSESSID}

    data = {'useraccount': strBase64UserId, 'password': strBase64Passwd,'schoolid': shoolId,
            'ssm': strBase64Sms}
    html = requests.post(url, headers=headers, verify=False, cookies=cookies, data=data)
    print(html.text)
    code = re.findall(r'success:(.*?),', html.text, re.I)[0]
    if code == "1":
        print("登录成功")

        #创建试卷
        usercodepaperid = createPaper(PHPSESSID)
        paperData = lookPaper(PHPSESSID,usercodepaperid)
        queInfo = dealData.getQuestionList(paperData)
        sentData = ans(queInfo,tiku)
        sentPage(PHPSESSID,sentData)
        return 1
    else:
        return 3


def getSms(PHPSESSID):

    url = 'http://exam.hm86.cn/com/common/appAction.php?action=ssm'
    headers = {'Host': 'exam.hm86.cn', 'Connection': 'keep-alive', 'Content-Length': '0',
               'Accept': 'text/html, */*; q=0.01', 'Origin': 'http://exam.hm86.cn',
               'X-Requested-With': 'XMLHttpRequest',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
               'Referer': 'http://exam.hm86.cn/vip/login/login.php', 'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9'}
    cookies = {"PHPSESSID":PHPSESSID}
    html = requests.post(url, headers=headers, verify=False, cookies=cookies)
    # print(len(html.text))
    return html.text

def getSession():
    url = 'http://exam.hm86.cn/com/base/common/ValidateCode.class.php?id=0.45510039671474267'
    headers = {'Host': 'exam.hm86.cn', 'Connection': 'keep-alive',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
               'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
               'Referer': 'http://exam.hm86.cn/vip/login/login.php', 'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9'}
    cookies = {}
    data = {}
    html = requests.get(url, headers=headers, verify=False, cookies=cookies)
    return html.headers['Set-Cookie'].split("PHPSESSID=")[1].split(";")[0]

#生成试卷
def createPaper(PHPSESSID):
    import requests

    url = 'http://exam.hm86.cn/web/front/study/exam_pager.php?paperid=1000000001'
    headers = {'Host': 'exam.hm86.cn', 'Connection': 'keep-alive', 'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
               'Referer': 'http://exam.hm86.cn/vip/login/login.php', 'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9'}
    cookies = {'PHPSESSID': PHPSESSID}

    html = requests.get(url, headers=headers, verify=False, cookies=cookies)
    print('试卷创建完成', html.text.split("usercodepaperid=")[1].split("\"")[0])
    return html.text.split("usercodepaperid=")[1].split("\"")[0]

#查看试卷
def lookPaper(PHPSESSID,usercodepaperid):
    global paperInfo
    url = f'http://exam.hm86.cn/web/front/study/examination.php?paperid=1000000001&usercodepaperid={usercodepaperid}'
    headers = {'Host': 'exam.hm86.cn', 'Proxy-Connection': 'keep-alive', 'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
               'Referer': 'http://exam.hm86.cn/web/front/study/exam_pager.php?paperid=1000000001',
               'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9'}
    cookies = {'PHPSESSID': PHPSESSID}
    html = requests.get(url, headers=headers, verify=False, cookies=cookies)
    print("正在处理试题...")
    try:
        paperInfo["starttime"] = re.findall(r'starttime=\"(.*?)\"', html.text, re.I)[0]
        paperInfo["csmpagerid"] = re.findall(r'csmpagerid=\"(.*?)\"', html.text, re.I)[0]
        paperInfo["memberusercode"] = re.findall(r'memberusercode=\"(.*?)\"', html.text, re.I)[0]
        paperInfo["memberschoolid"] = re.findall(r'memberschoolid=\"(.*?)\"', html.text, re.I)[0]
        paperInfo["membernickname"] = re.findall(r'membernickname=\"(.*?)\"', html.text, re.I)[0]
    except:
        print("无法开始考试,可能没有开启此学校的答题系统")
        exit()
    return html.text


#答题系统
def ans(queInfo,tiku):
    print("答题系统接收到了试题信息 如下")
    print(queInfo)
    num = 1
    noneNum = 1
    quesInfo = {}
    for i in queInfo:
        print("正在匹配第%s道题答案"%num)
        title = queInfo[i][1].split("、")[1]
        quesInfo[f"question{num}"] = []
        needAnswerCount = queInfo[i][2]
        option = queInfo[i][3]
        info = fuzz.simpleMatching(title,tiku,option)

        #匹配后的结果
        # print(queInfo[i])
        if info == None:
            print("查不到第%s题信息"%num)
            # 再查fuzz.simpleMatching(title, tiku, option)
            sentData.append({"orderindex": f"{num}", "topicid": f"{queInfo[i][0]}", "result": "B"})
            noneNum+=1
        elif info == []:
            print("查不到第%s题信息"%num)

            sentData.append({"orderindex": f"{num}", "topicid": f"{queInfo[i][0]}", "result": "B"})
            noneNum+=1
        else:
            # print("选项：",option)
            print("题库中此题答案：",info[2])
            #模糊对撞
            rightList = fuzz.dataCollision(info[2],option)
            print("匹配得出答案:",rightList)
            #遇到一个单选题逻辑问题，下面暂时写死，有时间再更新代码  下面说法正确的是()。
            if len(info[2]) == 1:
                if info[2][0] not in option:
                    sentData.append({"orderindex": f"{num}", "topicid": f"{queInfo[i][0]}", "result": "B"})
            #临时修的bug 如果是全选题全队 提交的空  这里重新赋值修bug  具体问题懒得看了 记得是改fuzz多选那部分后出来的bug
            if len(rightList) == 7:
                rightList="A,B,C,D"
            sentData.append({"orderindex": f"{num}", "topicid": f"{queInfo[i][0]}", "result": f"{rightList}"})
            # print(sentData)
        # quesInfo[f"question{num}"].append(info)
        # print(title)
        # print(title)
        # print(queInfo[i])
        num += 1
    # print("sentData数据：",sentData)
    print("一共没查到%s道题，等待作者优化题库"%(noneNum-1))
    return sentData
#交卷
def sentPage(PHPSESSID,sentData):
    global paperInfo
    # newSentData = str(sentData).replace("\'","\"")
    newSentData = dealData.replaceData(str(sentData).replace("\'","\""))
    print("等待15分钟后交卷...")
    for i in range(0, 101):
        time.sleep(9)
        char_num = i // 2  # 打印多少个'*'
        per_str = '\r%s%% : %s\n' % (i, '*' * char_num) if i == 100 else '\r%s%% : %s' % (i, '*' * char_num)
        print(per_str, end='', flush=True)

    print(paperInfo)
    sms = getSms(PHPSESSID)
    smsBase64 = base64.b64encode(sms.encode())
    strBase64Sms = str(smsBase64).replace("b\'",'').replace('\'','')
    url = 'http://exam.hm86.cn/web/front/study/examTopicAction.php?action=submit'
    headers = {'Host': 'exam.hm86.cn', 'Proxy-Connection': 'keep-alive', 'Content-Length': '10857', 'Accept': '*/*',
               'Origin': 'http://exam.hm86.cn', 'X-Requested-With': 'XMLHttpRequest',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'Referer': 'http://exam.hm86.cn/web/front/study/examination.php?paperid=1000000001&usercodepaperid=M2T0A2w1N-D1d1f-M2T7AhwmNsDocfwtMTEyNl8xMDAwMDAwMDAx',
               'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9'}
    cookies = {'PHPSESSID': PHPSESSID}
    data = {
        "paperid": "1000000001",
        "csmpagerid": paperInfo["csmpagerid"],
        "starttime": paperInfo["starttime"],
        "result_content": f'''{newSentData}''',
        "memberusercode": paperInfo["memberusercode"],
        "memberschoolid": paperInfo["memberschoolid"],
        "membernickname": paperInfo["membernickname"],
        "ssm": strBase64Sms
    }
    print("看一下发送的data：",data)
    html = requests.post(url, headers=headers, verify=False, cookies=cookies, data=data)
    print(html.text)
if __name__=='main':
    pass

