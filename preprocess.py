import Utils
import 关系提取.bikeOperation as bo
import os
import numpy as np
import jieba

#将组卷网映射到的所有的百度百科知识点放到一个集合中
def getBikeWordSet():
    file = open("F:\学习\一课一练\实验结果\映射的叶子知识点.txt", "r", encoding="utf-8")
    bikeWordSet = set()
    for line in file:
        bikeWords = line.split(":")[1].replace("\n", "").split(" ")
        for bikeWord in bikeWords:
            if bikeWord == "":
                continue
            if bikeWord.find(">") != -1:
                bw = bikeWord.split(">")[0]
            elif bikeWord.find("#") != -1:
                bw = bikeWord.split("#")[0]
            else:
                bw = bikeWord

            bikeWordSet.add(bw)
    return bikeWordSet

#根据百科词条爬取百科内容
def getBikeWordContent():
    bikeWordSet = getBikeWordSet()
    i = 1
    titleSet = set()
    for bikeword in bikeWordSet:
        res = bo.parseContent(bikeword)
        Utils.writeFile("../bikewordContent/"+bikeword+".txt",res[1])
        titleSet = titleSet | res[0]
        print(i)
        i+=1
    titles = ""
    for title in titleSet:
        titles += title+" "
    Utils.writeFile("titles.txt",titles)

#生成wordBase.txt文件，用于分词
def generateWordBase():
    words = getBikeWordSet()
    c = ""
    for word in words:
        c += word+"\n"
    Utils.writeFile("wordBase.txt",c)

#生产bikeWords,txt文件，用于保存所有知识点
def generateBikeWords():
    words = getBikeWordSet()
    c = ""
    for word in words:
        c += word + " "
    Utils.writeFile("bikeWords.txt", c)

def isContain(title,keyWord):
    if title.find(keyWord) != -1:
        return True
    return False

def generateTitleMapping():
    file = open("titles.txt","r",encoding="utf-8")
    line = file.readline()
    titles = line.split(" ")
    mapping = []
    mapping.append("历史")
    mapping.append("性质")
    mapping.append("简介")
    mapping.append("证明")
    mapping.append("方法")
    mapping.append("题解")
    mapping[0] = []
    mapping[1] = []
    mapping[2] = []
    mapping[3] = []
    mapping[4] = []
    mapping[5] = []
    for title in titles:
        if isContain(title,"史"):
            mapping[0].append(title)
        elif isContain(title,"性质") or isContain(title,"定义") or isContain(title,"意义") or isContain(title,"要点"):
            mapping[1].append(title)
        elif isContain(title,"简介") or isContain(title,"特性"):
            mapping[2].append(title)
        elif isContain(title,"证明"):
            mapping[3].append(title)
        elif isContain(title,"法") or isContain(title,"定理") or isContain(title,"运算") or isContain(title,"公式") or isContain(title,"公里"):
            mapping[4].append(title)
        elif isContain(title, "题") or isContain(title, "解") or isContain(title, "示例") or isContain(title, "实例") or isContain(title, "范例")\
                or isContain(title, "例子") or isContain(title, "举例"):
            mapping[5].append(title)
        else:
            print(title)

# 对百度百科的内容进行分词
def splitWords():
    jieba.load_userdict("wordBase.txt")
    for fileName in os.listdir("../bikewordContent"):

        # 先将知识点的内容进行拼接
        content = ""
        file = open(os.path.join('%s%s' % ("../bikewordContent/", fileName)), 'r', encoding="utf-8")
        for line in file:
            content += line

        #进行分词
        words = list(jieba.cut(content))

        #进行存储
        content = ""
        for w in words:
            content += w+" "
        Utils.writeFile("../splitedBikeContent/"+fileName,content)

#生成百度百科知识点的包含矩阵
def generateOccurrenceMatrix():
    jieba.load_userdict("wordBase.txt")
    #先读出所有百科词语
    file = open("bikeWords.txt", 'r', encoding='utf-8')
    line = file.readline()
    bikewords = line.split(" ")

    #初始化包含矩阵
    matrix = np.zeros((len(bikewords), len(bikewords)),dtype=np.int)


    for fileName in os.listdir("../splitedBikeContent"):
        currentBikeWord = fileName.split(".")[0]
        # print(currentBikeWord)
        #读取每个知识点对应的分词后的百度百科
        content = []
        file = open(os.path.join('%s%s' % ("../splitedBikeContent/", fileName)), 'r', encoding="utf-8")
        for line in file:
            for w in line.split(" "):
                content.append(w)

        for i,bikeword in enumerate(bikewords):
            count = content.count(bikeword)
            matrix[bikewords.index(currentBikeWord)][i] = count
        print(matrix[bikewords.index(currentBikeWord)])
    np.save("occurrenceMatrix.npy",matrix)

# #爬取组卷网映射的所有的百科词条的百科内容
# getBikeWordContent()

#根据bikeWrodSet去生成wordBase.txt，为了分词
# generateWordBase(getBikeWordSet())

# generateOccurrenceMatrix()