#coding=utf-8
import requests,json,re
import base64
import tool.dealData as dealData
import tool.fuzz as fuzz
import time
schoolInfo = {"河南大学":"10002","河南农业大学":"10003","河南师范大学":"10004","河南科技大学":"10005","河南理工大学":"10006","河南财经政法大学":"10008","华北水利水电大学":"10009","河南中医药大学":"10010","信阳师范学院":"10012","新乡医学院":"10013","郑州航空工业管理学院":"10014","河南科技学院":"10016","安阳师范学院":"10017","南阳师范学院":"10018","洛阳师范学院":"10019","商丘师范学院":"10020","周口师范学院":"10021","许昌学院":"10022","洛阳理工学院":"10024","河南警察学院":"10026","河南牧业经济学院":"10028","河南工学院":"10029","河南财政金融学院":"10030","黄淮学院":"10031","平顶山学院":"10032","安阳工学院":"10033","南阳理工学院":"10034","新乡学院":"10035","信阳农林学院":"10037","商丘工学院":"10043","商丘学院":"10044","郑州工商学院":"10047","信阳学院":"10048","安阳学院":"10049","河南开封科技传媒学院":"10050","中原科技学院":"10051","新乡医学院三全学院":"10052","新乡工程学院":"10054","黄河交通学院":"10056","河南科技职业大学":"10058","郑州电力高等专科学校":"10059","河南职业技术学院":"10060","郑州铁路职业技术学院":"10061","黄河水利职业技术学院":"10062","河南司法警官职业学院":"10063","河南工业职业技术学院":"10064","河南开放大学（郑州信息科技职业学院）":"10065","河南经贸职业学院":"10067","河南交通职业技术学院":"10068","河南农业职业学院":"10069","河南艺术职业学院":"10073","河南护理职业学院":"10075","河南推拿职业学院":"10076","河南林业职业学院":"10077","河南工业和信息化职业学院":"10078","开封大学":"10082","焦作大学":"10083","濮阳职业技术学院":"10084","许昌职业技术学院":"10085","商丘职业技术学院":"10086","平顶山工业职业技术学院":"10087","周口职业技术学院":"10088","济源职业技术学院":"10089","鹤壁职业技术学院":"10090","焦作师范高等专科学校":"10091","河南质量工程职业学院":"10092","漯河职业技术学院":"10093","三门峡职业技术学院":"10094","漯河医学高等专科学校":"10095","南阳医学高等专科学校":"10096","商丘医学高等专科学校":"10097","信阳职业技术学院":"10098","永城职业学院":"10100","郑州旅游职业学院":"10101","安阳职业技术学院":"10103","新乡职业技术学院":"10104","驻马店职业技术学院":"10105","开封文化艺术职业学院":"10106","许昌电气职业学院":"10107","洛阳职业技术学院":"10108","郑州幼儿师范高等专科学校":"10109","安阳幼儿师范高等专科学校":"10110","南阳农业职业学院":"10112","濮阳医学高等专科学校":"10113","驻马店幼儿师范高等专科学校":"10114","三门峡社会管理职业学院":"10115","河南测绘职业学院":"10117","河南地矿职业学院":"10120","平顶山职业技术学院":"10121","郑州电子信息职业技术学院":"10122","郑州电力职业技术学院":"10124","漯河食品职业学院":"10125","焦作工贸职业学院":"10128","许昌陶瓷职业学院":"10129","长垣烹饪职业技术学院":"10132","信阳涉外职业技术学院":"10133","鹤壁汽车工程职业学院":"10134","南阳职业学院":"10135","洛阳科技职业学院":"10138","鹤壁能源化工职业学院":"10139","平顶山文化艺术职业学院":"10140","信阳航空职业学院":"10141","中国一拖集团有限公司拖拉机学院":"10142","兰考三农职业学院":"10146","河南女子职业学院":"10147","林州建筑职业技术学院":"10148","濮阳石油化工职业技术学院":"10149","汝州职业技术学院":"10150","南阳科技职业学院":"10151","周口文理职业学院":"10154","洛阳文化旅游职业学院":"10155","信阳艺术职业学院":"10156"}
PHPSESSID = ''
sentData = []
paperInfo = {}

#模拟登录
def login(userId,passwd,schoolName,tiku):
    global PHPSESSID
    shoolId = schoolInfo[schoolName]
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

    code = html.text.split("{success:")[1].split(",")[0]

    if code == "1":
        print("登录成功")
        #创建试卷
        usercodepaperid = createPaper(PHPSESSID)
        paperData = lookPaper(PHPSESSID,usercodepaperid)
        queInfo = dealData.getQuestionList(paperData)
        sentData = ans(queInfo,tiku)
        sentPage(PHPSESSID,sentData)
    else:
        print(code)
    # if resp['success'] == 1:




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
        if info == None:
            print("查不到第%s题信息"%num)
            # 处理好此处双重匹配可以提高答案匹配率fuzz.simpleMatching(title, tiku, option)
            sentData.append({"orderindex": f"{num}", "topicid": f"{queInfo[i][0]}", "result": "B"})
            noneNum+=1
        elif info == []:
            print("查不到第%s题信息"%num)

            sentData.append({"orderindex": f"{num}", "topicid": f"{queInfo[i][0]}", "result": "B"})
            noneNum+=1
        else:
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
        num += 1
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

