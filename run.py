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

generateRelationByRefD()
br.getDirectedRelation()

# init = br.init()
# matrix = init[0]
# zeta = init[1]
# refd = br.RefD(matrix, 5, 185)
# print(refd)