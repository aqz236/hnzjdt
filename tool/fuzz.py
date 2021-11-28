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
   
            checkList[i] = like
        else:
            pass
    try:
        for oo in checkList:
            checkAns = tiku[oo]
            if checkAns[0] in option:
                return [oo, like, checkAns]
    except:
        pass

#数据对撞
def dataCollision(ansList, quesList, title, tiku):
    #多选
    quesDic = {}
    xuanxiang = ["A","B","C","D"]
    num = 0
    #给这道题选项编号 {"A":"选项1","B":"选项2"}
    for i in quesList:
        quesDic[xuanxiang[num]] = i
        num+=1
    print("看一下此题选项列表:",quesDic)
    if len(ansList) > 1:
        rightList = dataCollision2(ansList, quesDic, title, tiku, quesList)
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
    # # quesDic =  {'A': ' 真实的 ', 'B': '半真半假的 ', 'C': '虚幻的 '} 这题的乱序选项字典
    # title 这题的题目
    #tike 题库
    #quesList 这题的乱序选项
    checkList = {}

    for i in tiku:
        titleLike = fuzz.ratio(title, i)  # 在题库中匹配答案
        #如果匹配到了即完美匹配 就返回
        if titleLike == 100:
            daanliebiao = tiku[i]#拿到答案列表
            rightKeyList = []
            #选项进行排序
            for iii in quesDic:
                for ppp in daanliebiao:
                    like = fuzz.ratio(ppp, quesDic[iii])  # 答案相似度
                    if like > 88:#得出选项列表['A','B','C']
                        rightKeyList.append(iii)
            return rightKeyList

        #非完美匹配  双重匹配
        elif titleLike > 60 and titleLike != 100:#题目比较相似
            #对答案进行匹配
            quesDicToList = []
            for item in quesDic:
                quesDicToList.append(quesDic[item])
            answerLike = fuzz.ratio(','.join(set(ansList)), ','.join(set(quesDicToList)))#答案整体相似度
            if answerLike > 35:
                doubleLike = titleLike + answerLike
                checkList[i] = doubleLike

        elif titleLike > 60 and titleLike != 100:  # 题目比较相似
            allLikeValue = {}
            addLikeValue = 0
            # 双重匹配  开始匹配答案相似度
            quesDicToList = []
            for item in quesDic:#字典转列表
                quesDicToList.append(quesDic[item])
            answerLike = fuzz.ratio(','.join(set(ansList)), ','.join(set(quesDicToList)))  # 答案整体相似度
            addLikeValue = titleLike + answerLike
            checkList[i] = addLikeValue  # 题目对应总相似度


    # print('最大', tiku[max((checkList))])#筛选出组合相似度最大的答案选项
    rightKeyList = []
    # 选项进行排序
    try:
        maxCheckList = tiku[max((checkList))]
        for iii in quesDic:
            for ppp in maxCheckList:
                like = fuzz.ratio(ppp, quesDic[iii])  # 答案相似度
                if like > 88:  # 得出选项列表['A','B','C']
                    rightKeyList.append(iii)
        return rightKeyList
    except:
        return ['A','B']

