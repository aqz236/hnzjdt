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

    # print('试卷创建完成', html.text.split("usercodepaperid=")[1].split("\"")[0])
    try:
        usercodepaperid = re.findall(r'usercodepaperid=(.*?)>', html.text, re.I)[0].replace("\'","").replace("\"",'')
        print("试卷创建完成",usercodepaperid)
    except Exception as e:
        print("获取usercodepaperid失败，2021-12-02 v1.62")

    return usercodepaperid

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
        print("无法开始考试，可能原因：")
        print("1、网站暂未开启该学校的考试系统【如何验证：去网站登录页面看学校选择框里是否在里面】")
        print("如何修复：请前往https://github.com/aqz236/hnzjdt提交issues")
    return html.text


#答题系统
def ans(queInfo,tiku):
    print("答题系统接收到了试题信息")
    num = 1
    noneNum = 1
    quesInfo = {}

    for i in queInfo:
        print("正在匹配第%s道题答案"%num)
        titleNumber = queInfo[i][1].split("、")[0]
        title = queInfo[i][1].replace(titleNumber+"、",'')
        quesInfo[f"question{num}"] = []
        needAnswerCount = queInfo[i][2]
        option = queInfo[i][3]
        info = fuzz.simpleMatching(title,tiku,option)



        #匹配后的结果
        # print(queInfo[i])
        if info == None:
            print("None查不到第%s题信息"%num)
            print("这题的题目:",title)
            print("这题的选项:",option)
            # 再查fuzz.simpleMatching(title, tiku, option)
            sentData.append({"orderindex": f"{num}", "topicid": f"{queInfo[i][0]}", "result": "B"})
            noneNum+=1

        elif info == []:
            print("[]查不到第%s题信息"%num)
            print(title)
            sentData.append({"orderindex": f"{num}", "topicid": f"{queInfo[i][0]}", "result": "B"})
            noneNum+=1
        else:
            # print("选项：",option)
            rightList = fuzz.dataCollision(info, option, title, tiku)
            if rightList == '' or rightList ==None or rightList == "":
                print("--------------------------------------------------")
                print("此题查不到，默认选了A 希望可以前往https://github.com/aqz236/hnzjdt提交issues，下面是这个题的题目")
                sentData.append({"orderindex": f"{num}", "topicid": f"{queInfo[i][0]}", "result": "A"})
                print("--------------------------------------------------")
                noneNum += 1
            else:
                print("题目：", title)
                print("选项：",option)
                print("题库中此题答案：", info)
                print("匹配得出：", rightList)
                sentData.append({"orderindex": f"{num}", "topicid": f"{queInfo[i][0]}", "result": f"{rightList}"})
        num += 1
    if noneNum-1 == 0:
        print("☆*: .｡. o(≧▽≦)o .｡.:*☆全部匹配成功")
    else:
        print("一共没查到%s道题，等待作者优化题库"%(noneNum-1))
    return sentData
#交卷
def sentPage(PHPSESSID,sentData):
    global paperInfo
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
               'Referer': 'http://exam.hm86.cn/web/front/study/examination.php?paperid=1000000001',
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
    #print("newSentData":newSentData)
    html = requests.post(url, headers=headers, verify=False, cookies=cookies, data=data)
    print(html.text)
if __name__=='main':
    pass

