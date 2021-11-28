from fuzzywuzzy import fuzz
def simpleMatching(title,tiku,option):
    num = 1
    dataList = []
    checkList = {}
    #一个标题可能搜到多个答案，进行相似度比对
    like = 0
    for i in tiku:
        like = fuzz.ratio(title, i)
        #题目相似度
        if like >68:
            #如果遇到题目相似，答案不同。  做相似度对比 取最大相似度对应的信息，
            checkList[i] = like
        else:
            pass
    try:
        #一个题目匹配到多个答案就检查答案存在否
        for oo in checkList:
            checkAns = tiku[oo]
            if checkAns[0] in option:
                return [oo, like, checkAns]
        # checkedTitle = max(checkList, key=checkList.get)
    except:
        pass

#数据对撞
def dataCollision(ansList, quesList, title, tiku):
    #多选
    quesDic = {}
    xuanxiang = ["A","B","C","D"]
    num = 0
    for i in quesList:
        quesDic[xuanxiang[num]] = i
        num+=1
    if len(ansList) > 1:
        rightList = dataCollision2(ansList, quesDic, title, tiku, quesList)
        print("rightList::",rightList)
        return ','.join(set(rightList))
    #单选
    elif len(ansList) == 1:
        rightList = dataCollision1(ansList,quesList)
        return ','.join(set(rightList))
    else:
        print("答案选择器出错")
#单选
def dataCollision1(ansList,quesList):
    num = 1
    rightKeyList = []
    for i in ansList:
        contrastList = {}
        for o in quesList:
            like = fuzz.ratio(i, o)
            if like > 68:
                index = quesList.index(str(o))
                rightKey = str(index+1).replace('1','A').replace('2','B').replace('3','C').replace('4','D')
                contrastList[str(i)+f'&&&{rightKey}&&&'+str(o)] = like
            else:
                pass
        num+=1
        try:
            a = max(contrastList,key = contrastList.get)
            rightKey = a.split("&&&")[1]
            rightKeyList.append(rightKey)
        except:
            pass

    return rightKeyList
#多选
def dataCollision2(ansList, quesDic, title, tiku, quesList):
    # # ansList = ['真实的', '虚幻的']
    # # quesDic =  {'A': ' 真实的 ', 'B': '半真半假的 ', 'C': '虚幻的 '}
    # title 这题的题目
    checkList = {}
    for i in tiku:
        titleLike = fuzz.ratio(title, i)  # 题目相似度
        if titleLike == 100:
            checkList[i] = 100# 完美匹配
            print("完美匹配")
            rightAnswerList = tiku[max((checkList))]#取答案列表
            rightKeyList = []
            #答案匹配
            for ii in quesDic:
                for pp in rightAnswerList:
                    like = fuzz.ratio(pp, quesDic[ii])#答案相似度
                    if like > 88:
                        rightKeyList.append(ii)
            checkList.clear()
            return rightKeyList

        if titleLike > 60 and titleLike != 100: #题目较为相似
            # 双重匹配  开始匹配答案相似度
            quesDicToList = []
            for item in quesDic:
                quesDicToList.append(quesDic[item])
            answerLike = fuzz.ratio(','.join(set(ansList)), ','.join(set(quesDicToList)))
            if answerLike > 45:
                #数据对撞
                rightKeyList = []
                for ii in quesDic:
                    for pp in ansList:
                        like = fuzz.ratio(pp, quesDic[ii])
                        if like > 88:
                            rightKeyList.append(ii)
                return rightKeyList

            else:
                #正常是到不了这里的，如果题库更新 防止找不到题目就默认返回[A,B,C,D]
                rightKeyList = ["A","B","C","D"]
                return rightKeyList
        else:
            pass




