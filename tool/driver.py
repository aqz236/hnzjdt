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
        print("无法开始考试，可能原因：")
        print("1、网站暂未开启该学校的考试系统【如何验证：去网站登录页面看学校选择框里是否在里面】")
        print("如何修复：请前往https://github.com/aqz236/hnzjdt提交issues")
    return html.text


#答题系统
def ans(queInfo,tiku):
    print("答题系统接收到了试题信息")
    # print(queInfo)
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
        if info == None:
            print("*************************************************")
            print("None查不到第%s题信息"%num)
            print("此题查不到，希望可以前往https://github.com/aqz236/hnzjdt提交issues，下面是这个题的题目")
            print(title)
            print("下面是这题的选项")
            print(option)
            print("*************************************************")

            sentData.append({"orderindex": f"{num}", "topicid": f"{queInfo[i][0]}", "result": "B"})
            noneNum+=1
        elif info == []:
            print("[]查不到第%s题信息"%num)
            print("此题查不到，希望可以前往https://github.com/aqz236/hnzjdt提交issues，下面是这个题的题目")

            print(title)
            sentData.append({"orderindex": f"{num}", "topicid": f"{queInfo[i][0]}", "result": "B"})
            noneNum+=1
        else:
            # print("选项：",option)
            #模糊对撞 1.3版本双重匹配
            print(title)
            
            rightList = fuzz.dataCollision(info[2], option, title, tiku)
            print("题库中此题答案：", info[2])
            print("匹配得出答案:", rightList)
            print("选项已自动排序")
            if len(info[2]) == 1:
                if info[2][0] not in option:
                    sentData.append({"orderindex": f"{num}", "topicid": f"{queInfo[i][0]}", "result": "B"})
            #临时修的bug 如果是全选题全队 提交的空  这里重新赋值修bug  具体问题懒得看了 记得是改fuzz多选那部分后出来的bug
            if len(rightList) == 7:
                rightList="A,B,C,D"
            sentData.append({"orderindex": f"{num}", "topicid": f"{queInfo[i][0]}", "result": f"{rightList}"})
        num += 1
    # print("sentData数据：",sentData)
    print("一共没查到%s道题，等待作者优化题库"%(noneNum-1))
    print("希望可以前往https://github.com/aqz236/hnzjdt提交issues，协助作者更新题库")
    return sentData
#交卷
def sentPage(PHPSESSID,sentData):
    global paperInfo
    newSentData = dealData.replaceData(str(sentData).replace("\'","\""))
    print("等待15分钟后交卷...")
    for i in range(0, 101):
        char_num = i // 2  # 打印多少个'*'
        per_str = '\r%s%% : %s\n' % (i, '*' * char_num) if i == 100 else '\r%s%% : %s' % (i, '*' * char_num)
        print(per_str, end='', flush=True)
        time.sleep(9)

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
    html = requests.post(url, headers=headers, verify=False, cookies=cookies, data=data)
    print(html.text)
    print("执行完毕，你的星星是给我的最大支持")
    print("项目地址：https://github.com/aqz236/hnzjdt")
if __name__=='main':
    pass

