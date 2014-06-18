# -*- coding: utf-8 -*-
import math

EQUITY = 7597952860.16
D = 5327417411
R = 0.0281
T = 1

def get_listP(filename):
    file = open(filename) # 返回一个文件对象
    listP = []
    while 1:
        lines = file.readlines(300) # 调用文件的 readline()方法
        if not lines:
            break;
        for line in lines:
            listP.append(float(line.rstrip())) # 后面跟 ',' 将忽略换行符
            # print(line, end = '')　　在 Python 3中使用
    file.close()
    return listP

def get_sigmaP(listP):
    # N 个股票价格推出 N-1 个股票价格的日收益率
    listU = []
    sumU = 0.0
    for i in range(1, N):
        u = math.log(listP[i] / listP[i-1])
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
    sigmaPDay = math.sqrt(dayYieldVariance / (N-2))
    return (sigmaPDay * math.sqrt(N-1))

def get_sigmaV0(sigmaP):
    numerator = EQUITY * sigmaP
    denominator = EQUITY + (D * math.pow(math.e, -R * T))
    return (numerator / denominator)

def get_nd2(sigmaP, sigmaV0):
    numerator = (sigmaP - sigmaV0) * EQUITY
    denominator = sigmaV0 * D * math.pow(math.e, -R * T)
    return numerator / denominator

def find_word(filename, word):
    with open(filename, 'r') as f:
        for l in f.readlines():
              if word in l:
                    if word == l.split()[0] :
                        return float(l.split()[1])

def get_d2(nd2, filename):
    if 0 < nd2 < 0.5 :
        return -find_word(filename,  '%.5f' % (1-nd2))
    elif nd2 == 0.5 :
        return 0
    elif 0.5 < nd2 < 1 :
        return find_word(filename,  '%.5f' % nd2)
    else :
        return 9999

def get_nd1(d1, filename):
    # print d1
    if d1 > 0:
        return find_word(filename, '%.4f' % d1)
    elif d1 < 0:
        return 1 - find_word(filename, '%.4f' % (-d1))
    else :
        return 0.5

def get_fd1(sigmaP, sigmaVi, nd1, d1, nd2):
    temp = math.log((EQUITY + (D * math.pow(math.e, -R * T) * nd2) / (nd1 * D)))
    numerator = temp + (R + 0.5 * sigmaVi * sigmaVi) * T
    denominator = sigmaVi * math.sqrt(T)
    fund1i = (d1 - numerator / denominator)
    if fund1i < 0 :
        fund1i = -fund1i
    # print fund1i
    return fund1i


def get_fund1(sigmaP, sigmaVi, nd1, d1):
    temp = math.log((sigmaP * EQUITY) / (nd1 * sigmaVi * D))
    numerator = temp + (R + 0.5 * sigmaVi * sigmaVi) * T
    denominator = sigmaVi * math.sqrt(T)
    fund1i = (d1 - numerator / denominator)
    if fund1i < 0 :
        fund1i = -fund1i
    # print fund1i
    return fund1i

def get_v(sigmaP, nd1, sigmaV):
    numerator = sigmaP * EQUITY
    denominator = nd1 * sigmaV
    return numerator / denominator

def get_v2(sigmaV, nd1, nd2):
    numerator = D * math.pow(math.e, -R * T) * nd2 + EQUITY
    denominator = nd1
    return numerator / denominator

def main():
    global N
    global EQUITY
    global D
    global R
    global T
    # read price of stock from file "stock-price"
    listP = get_listP("stock-price")
    N = len(listP)
    sigmaP = get_sigmaP(listP)
    print "The volatility of the stock's price: sigmaP = %10.12f" % sigmaP
    sigmaVi = sigmaV0 = get_sigmaV0(sigmaP) # sigmaV0 is the down limit
    # print sigmaV0
    sigmaV = nd1 = 0.0
    fund1 = 99999
    while True :
        sigmaVi += 0.0001
        if sigmaVi > sigmaP :
            break
        nd2i = get_nd2(sigmaP, sigmaVi)
        d2i = get_d2(nd2i, "nx-x")
        if d2i == 9999 :
            continue
        d1i = sigmaVi * T + d2i
        nd1i = get_nd1(d1i, "x-nx")
        fund1i = get_fund1(sigmaP, sigmaVi, nd1i, d1i)
        # fund1i = get_fd1(sigmaP, sigmaVi, nd1i, d1i, nd2i)
        if fund1 > fund1i :
            fund1 = fund1i
            sigmaV = sigmaVi
            nd1 = nd1i
        # print "The fund1i is %10.12f, and the sigmaVi is %10.12f" % (fund1i, sigmaVi)
    print "The fd1 is %10.12f, and the sigmaV is %10.12f" % (fund1, sigmaV)
    v = get_v(sigmaP, nd1, sigmaV)
    # v = get_v2(sigmaP, nd1, sigmaV)
    print "V is %.10f" % v
    dd = (v - D) / (v * sigmaV)
    print "DD is %.10f" % dd
    edf = get_nd1(-dd, "x-nx")
    print "EDF is %.10f" % edf

if __name__=="__main__":
    main()
