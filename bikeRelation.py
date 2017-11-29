import numpy as np

#初始化函数
def init():
    #加载共现矩阵
    matrix = np.load("occurrenceMatrix.npy")
    zeta = 0.025
    return matrix,zeta


#matrix是共现矩阵
#A、B分别是知识点的索引
def RefD(matrix,A,B):
    #A知识点在所有知识点中的重要程度，即第A列的和
    impA = 0
    for i in matrix[:,A]:
        impA += 1

    # A知识点在AB共现的百科中的重要程度，即AB两列都不为0的行的值中，A的值的和
    impAtoAB = 0
    for i in range(0, matrix.shape[0] - 1):
        if matrix[i][B] != 0 and matrix[i][A] != 0:
            impAtoAB += 1

    # B知识点在所有知识点中的重要程度，即第B列的和
    impB = 0
    for i in matrix[:, B]:
       impB += 1

    #B知识点在AB共现的百科中的重要程度
    impBtoAB = 0
    for i in range(0,matrix.shape[0]-1):
        if matrix[i][B] != 0 and matrix[i][A] != 0:
            impAtoAB += 1


    if impA == 0:
        IA = 0
    else:
        IA = impAtoAB / impA
    if impB == 0:
        IB =0
    else:
        IB = impBtoAB/impB


    return IA - IB

relationMatrix = None
flagMatrix = None
path = []
def KMP(i,j):
    flagMatrix[i][j] = 1
    path.append()

def isCicle():
    for i in range(0,relationMatrix.shape[0]):
        for j in range(i+1,relationMatrix.shape[1]):
            if relationMatrix[i][j] !=0 and flagMatrix[i][j] ==0:
                KMP(i,j)

def getNextConceptsIndex(relationMatrix,index,deep):
    if deep>10:
        return []
    res = []
    for i in range(0,relationMatrix.shape[0]):
        if relationMatrix[index][i] != 0:
            res.append(i)
            nextConcepts = getNextConceptsIndex(relationMatrix,i,deep+1)
            for k in nextConcepts:
                res.append(k)
    return res

def removeMiddleRelation(relationMatrix):
    for i in range(0,relationMatrix.shape[0]):
        for j in range(0,relationMatrix.shape[1]):
            if relationMatrix[i][j] != 0:
                nextConcepts = getNextConceptsIndex(relationMatrix,j,0)
                for k in nextConcepts:
                    relationMatrix[i][k] = 0
    return relationMatrix

def getDirectedRelation():
    relationMatrix = np.load("relationMatrix.npy")
    print(len(relationMatrix[relationMatrix>0]))
    flagMatrix = np.zeros((relationMatrix.shape[0],relationMatrix.shape[1]),dtype=np.int8)
    # 中间关系消除
    directedRelationMatrix = removeMiddleRelation(relationMatrix)
    # np.save("directedRelationMatrix.npy",directedRelationMatrix)
    print(len(relationMatrix[directedRelationMatrix > 0]))
    printRelation(directedRelationMatrix)


def printRelation(relationMatrix):
    file = open("bikeWords.txt", 'r', encoding='utf-8')
    line = file.readline()
    bikewords = line.split(" ")

    for i in range(0,relationMatrix.shape[0]-1):
        for j in range(0,relationMatrix.shape[1]-1):
            if relationMatrix[i][j] != 0:
                print(relationMatrix[i][j],bikewords[i]+"--->"+bikewords[j])