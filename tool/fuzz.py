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
        #一个题目匹配到多个答案就检查答案存在否
        for oo in checkList:
            checkAns = tiku[oo]
            if checkAns[0] in option:
                return [oo, like, checkAns]
    except:
        pass

#数据对撞
def dataCollision(ansList,quesList):
    #多选
    quesDic = {}
    xuanxiang = ["A","B","C","D"]
    num = 0
    for i in quesList:
        quesDic[xuanxiang[num]] = i
        num+=1
    print("看一下此题选项列表:",quesDic)
    if len(ansList) > 1:
        rightList = dataCollision2(ansList,quesDic)
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
def dataCollision2(ansList, quesDic):
    #此处有个问题  如果一个题对应了多种答案就会选错 解决思路，再进行答案模糊匹配，即模糊匹配两次 如果通过则返回，有需要的自己写个逻辑
  
    rightKeyList = []
    for ii in quesDic:
        for pp in ansList:
            like = fuzz.ratio(pp, quesDic[ii])
            if like > 88:
                rightKeyList.append(ii)
    return rightKeyList




