import 关系提取.bikeRelation as br
import numpy as np

#使用RefD方生成关系矩阵
def generateRelationByRefD():
    init = br.init()
    matrix = init[0]
    zeta = init[1]
    relationMatrix = np.zeros((matrix.shape[0],matrix.shape[1]),dtype=np.double)
    for i in range(0, matrix.shape[0] - 1):
        for j in range(i+1, matrix.shape[0] - 1):
            refd = br.RefD(matrix, i, j)
            if refd > zeta:
                relationMatrix[j][i] = refd
            elif refd < -zeta:
                relationMatrix[i][j] = -refd
    np.save("relationMatrix.npy",relationMatrix)

# generateRelationByRefD()
# br.getDirectedRelation()

# 读取使用神经网络生成的关系
def generateRelationByW2V():
    file = open("bikeWords.txt", 'r', encoding='utf-8')
    line = file.readline()
    bikewords = line.split(" ")

    delta = 300
    ans = np.load("w1plusw2_multipliedby_w1plusw2.npy")
    # print(ans.shape)
    k = 0
    for i in range(0, ans.shape[0]-1):
        for j in range(0, ans.shape[0] - 1):
            if ans[i][j] > delta :
                print(ans[i][j], bikewords[i]+"--->"+bikewords[j])
                k+=1
            # elif ans[i][j] < -delta:
            #     print(ans[i][j], bikewords[j] + "--->" + bikewords[i])
    print("relation number:"+k)