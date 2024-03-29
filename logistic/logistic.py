import numpy as np
import matplotlib.pyplot as plt

def loadDataSet(file_name):
    """
    Desc:
        加载并解析数据
    Args:
        file_name -- 要解析的文件路径
    Returns:
        dataMat -- 原始数据的特征
        labelMat -- 原始数据的标签
    """
    #dataMat为原始数据， labelMat为原始数据的标签
    dataMat = []
    labelMat = []
    fr = open(file_name)
    for line in fr.readlines():
        lineArr = line.strip().split()
        #为了方便计算，我们将x0的值设为1.0， 也就是每一行的开头添加一个1.0作为x0
        dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])
        labelMat.append(int(lineArr[2]))

    return dataMat, labelMat


def sigmod(inX):
    #return 1.0 / (1 + exp(-inX))

    #tanh 是sigmod的变形
    return 2 * 1.0 / (1 + np.exp(-2 * inX)) - 1

#正常的处理方案
#两个参数，第一个参数==> dataMatIn 是一个2维numpy数组，每列分别代表每个不同的特征，每行则代表每个训练样本
#第二个参数 ==> classLabels 是类别标签，它是一个1 * 100的行向量，为了便于矩阵计算，需要将该行向量转换为列向量
def gradAscent(dataMatIn, classLabels):
    #转化为矩阵
    dataMatrix = np.mat(dataMatIn) #转换为numpy矩阵
    #将行向量转化为列向量
    labelMat = np.mat(classLabels).transpose()
    #m数据量，样本数， n特征数
    m, n = dataMatrix.shape
    #alpha = 0.001
    alpha = 0.01
    #迭代次数
    maxCycles = 2500
    #maxCycles = m
    print(m)
    #生成一个长充和特征数相同的矩阵，此处n = 3
    #weights代表回归系数，此处的ones((n, 1))创建一个长度和特征数相同的矩阵，基中的数全部是1
    weights = np.ones((n, 1))
    for i in range(maxCycles):
        #[m * 3] * [3 * 1] = [n * 1]
        #print(weights)
        #print(dataMatrix[i])
        h = sigmod((dataMatrix * weights))
        #labelMat是实际值
        error = (labelMat - h)
        #error = (classLabels[i] - h)
        # 0.001 * (3*m) * (m*1)表示在每一个列上的一个误差情况，最后得出x1, x2, xn的系数的偏移量

        weights = weights + alpha * dataMatrix.transpose() * error
        print('\n')
        print(error)
        print('\n')
        print(weights)
        print('\n')

    return np.array(weights)

def plotBestFit(dataArr, labelMat, weights):
    """
    Desc:
        将数据可视化得展示出来
    Args:
        dataArr:样本数据的特征
        labelMat:样本数据的标签
        weights:回归系数
    Returns:
        None
    """
    n = dataArr.shape[0]
    xcord1 = []; ycord1 = []
    xcord2 = []; ycord2 = []
    for i in range(n):
        if int(labelMat[i]) == 1:
            xcord1.append(dataArr[i, 1]); ycord1.append(dataArr[i, 2])
        else:
            xcord2.append(dataArr[i, 1]); ycord2.append(dataArr[i, 2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s = 30, c = 'red', marker = 's')
    ax.scatter(xcord2, ycord2, s = 30, c = 'green')
    x = np.arange(-3.0, 3.0, 0.1)
    """
    w0 * x0 + w1 * x1 + w2 * x2 = f(x)
    w0 + w1 * x + w2 * y = 0, f(x)整合到了w0, w1, w2上
    """
    y = (-weights[0] - weights[1] * x) / weights[2]
    ax.plot(x, y)
    plt.xlabel('X'); plt.ylabel('Y')
    plt.show()

def testLR():
    #1.收集并准备数据
    dataMat, labelMat = loadDataSet("TestSet.txt")

    #2.训练模型
    dataArr = np.array(dataMat)
    weights = gradAscent(dataArr, labelMat)

    #3.数据可视化
    plotBestFit(dataArr, labelMat, weights)

if __name__ == '__main__':
    testLR()
