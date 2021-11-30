import re
def getQuestionList(src_html):
    queInfo = {}
    aa = src_html.replace("\n","").replace("\t","")
    a = aa.split("<tr id=\"")
    TOPICIDData = src_html.split("topicJsonArray=")[1].split(";")[0]
    num = 1
    for i in a:
        try:
            queTopicid = i.split("topicid=\"")[1].split("\"")[0]
            ansNumber = len(i.split("<font class=\"f14\">"))-1
            queTitle = re.findall(r'line-height:30px;\">(.*?)</', i, re.I)[0].replace("\r","")
            queContentList = i.split("<font class=\"f14\">")
            thisAnsList = []
            for o in queContentList:
                try:
                    ans = o.split("</font>")[0]
                    thisAnsList.append(ans)
                except:
                    pass
            thisAnsList.pop(0)
            queList = [queTopicid,queTitle,ansNumber,thisAnsList]
            queInfo[f"que{num}"] = queList
            num+=1
        except Exception as e:
            # print(e,"网页可能已更新，请联系管理员更新dealData")
            pass
    print("处理完成")
    return queInfo

#选项重新排列 
def replaceData(data):
    newData = str(data).replace("B,A","A,B").replace("C,A","A,C").replace("D,A","A,D").replace("A,C,B","A,B,C") \
        .replace("B,A,C", "A,B,C").replace("B,C,A","A,B,C").replace("B,A,D","A,B,D").replace("B,D,A","A,B,D") \
        .replace("B,D,C", "B,C,D").replace("C,B,A","A,B,C").replace("C,A,B","A,B,C").replace("C,D,A","A,C,D") \
        .replace("C,A,D", "A,C,D").replace("D,A,B","A,B,D").replace("D,B,A","A,B,D").replace("D,C,B","C,B,D") \
        .replace("D,B,C", "B,C,D").replace("D,A,C","A,C,D").replace("D,C,A","A,C,D")\
        .replace("A,C,B,D","A,B,C,D").replace("A,C,D,B","").replace("A,B,D,C","").replace("B,A,C,D","") \
        .replace("B,C,D,A", "A,B,C,D").replace("B,D,A,C","A,B,C,D").replace("B,D,C,A","A,B,C,D").replace("C,A,B,D","A,B,C,D").replace("C,A,D,B","A,B,C,D") \
        .replace("C,B,A,D", "A,B,C,D").replace("D,A,B,C","A,B,C,D").replace("D,B,A,C","A,B,C,D").replace("D,C,A,B","A,B,C,D") \
        .replace("D,C,B,A", "A,B,C,D").replace("C,B,D,A","A,B,C,D").replace("D,A,C,B","A,B,C,D").replace("D,B,C,A","A,B,C,D")
    return newData

