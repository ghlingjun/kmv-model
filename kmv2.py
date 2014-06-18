# -*- coding: utf-8 -*-
import math

N = 0

def get_listE(filename):
    file = open(filename) # 返回一个文件对象
    listE = []
    while 1:
        lines = file.readlines(300) # 调用文件的 readline()方法
        if not lines:
            break;
        for line in lines:
            listE.append(float(line.rstrip())) # 后面跟 ',' 将忽略换行符
            # print(line, end = '')　　在 Python 3中使用
    file.close()
    return listE

def get_sigmaE(listE):
    listU = []
    sumU = 0.0
    for i in range(1, N):
        u = math.log(float(listE[i]) / float(listE[i-1]))
        # print u
        listU.append(u)
        sumU += u
    # print sumU
    avgU = sumU / (N - 1)
    # print "平均日收益率为: %10.12f" % avgU
    dayYieldVariance = 0.0
    for u in listU :
        dayYieldVariance += math.pow((u - avgU), 2)
        # print dayYieldVariance
    sigmaEDay = math.sqrt(dayYieldVariance / (N-2))
    return (sigmaEDay * math.sqrt(N-1))

def get_list_sigmaV0(listE, sigmaE, d, r, t):
    list_sigmaV = []
    # print "r is %10.12f, d is %d, t is %d\n" % (r, d, t)
    for i in range(0, N):
        # print listE[i]
        temp = listE[i] + (d * math.pow(math.e, -r * t))
        list_sigmaV.append(0.5 * sigmaE * (listE[i] / temp + 1))
    return list_sigmaV

def get_listNd2(listE, sigmaE, list_sigmaV, d, r, t):
    listNd2 = []
    for i in range(0, N):
        temp = d * math.pow(math.e, -r * t)
        listNd2.append(((sigmaE / list_sigmaV[i] - 1) / temp) * listE[i])
    return listNd2

def find_word(filename, word):
    with open(filename, 'r') as f:
        for l in f.readlines():
              if word in l:
                    if word == l.split()[0] :
                        return float(l.split()[1])

def get_listd2(listNd2, filename):
    listd2 = []
    for nd2 in listNd2 :
        if nd2 == 0 :
            listd2.append(0)
        elif 0 < nd2 < 0.5 :
            listd2.append(-find_word(filename,  '%.5f' % (1-nd2)))
        elif nd2 == 0.5 :
            listd2.append(0)
        elif nd2 == 1 :
            listd2.append(1)
        else :
            listd2.append(find_word(filename,  '%.5f' % nd2))
    return listd2

def get_listd1(listd2, list_sigmaV, t):
    listd1 = []
    for i in range(0, N):
        listd1.append(listd2[i] + list_sigmaV[i] * t)
    return listd1

def get_listNd1(listd1, filename):
    listNd1 = []
    for d1 in listd1 :
        if d1 > 0 :
            listNd1.append(find_word(filename,  '%.4f' % d1))
        elif d1 < 0 :
            temp = find_word(filename, '%.4f' % (-d1))
            listNd1.append(find_word(filename,  1 - temp))
        else :
            listNd1.append(0.5)
    return listNd1

def get_listW(listE, sigmaE):
    d = 5327417411
    r = 0.0281
    t = 1
    list_sigmaV = get_list_sigmaV0(listE, sigmaE, d, r, t)
    # print list_sigmaV
    listNd2 = get_listNd2(listE, sigmaE, list_sigmaV, d, r, t)
    # print listNd2
    listd2 = get_listd2(listNd2, "nx-x")
    # print listd2
    listd1 = get_listd1(listd2, list_sigmaV, t)
    # print listd1
    listNd1 = get_listNd1(listd1, "x-nx")
    # print listNd1
    listW = []
    for i in range(0, N):
        temp = listNd2[i] * math.pow(math.e, -r * t)
        listW.append(listNd1[i] * (listE[i] / d + temp))
    # print listW
    return listW

def get_listNd2i(listW, sigmaE, sigmaV, d, r, t):
    listNd2 = []
    for i in range(0, N):
        temp = d * math.pow(math.e, -r * t)
        listNd2.append(((sigmaE / sigmaV - 1) / temp) * listW[i])
    return listNd2

def get_listd1i(listd2, sigmaV, t):
    listd1 = []
    for i in range(0, N):
        listd1.append(listd2[i] + sigmaV * t)
    return listd1

def get_listWi(listW, sigmaE, sigmaV):
    d = 5327417411
    r = 0.0281
    t = 1
    listNd2 = get_listNd2i(listW, sigmaE, sigmaV, d, r, t)
    print listNd2
    listd2 = get_listd2(listNd2, "nx-x")
    # print listd2
    listd1 = get_listd1i(listd2, sigmaV, t)
    # print listd1
    listNd1 = get_listNd1(listd1, "x-nx")
    # print listNd1
    listWi = []
    for i in range(0, N):
        temp = listNd2[i] * math.pow(math.e, -r * t)
        listWi.append(listNd1[i] * (listE[i] / d + temp))
    return listWi

def main():
    # read equity from file "equity"
    listE = get_listE("equity")
    # print listE
    global N
    N = len(listE)
    # print N
    sigmaE = get_sigmaE(listE)
    print "The volatility of the value of equity:  sigmaE = %10.12f" % sigmaE
    listW = get_listW(listE, sigmaE)
    sigmaV1 = get_sigmaE(listW)
    print "sigma V1 is: %10.12f" % sigmaV1

    sigmaV2 = 0.0
    i = 0
    while True:
        i += 1
        listW = get_listWi(listW, sigmaE, sigmaV1)
        # print listW
        sigmaV2 = get_sigmaE(listW)
        print "sigma V%d is: %10.12f" % (i, sigmaV2)
        diff = abs(sigmaV2 - sigmaV1)
        print diff
        if diff <= 0.000001 :
            break
    sigmaV = sigmaV2
    print "The final sigmaV is: " + str(sigmaV)

if __name__=="__main__":
    main()
