# -*- coding: utf-8 -*-
import math, sys, getopt

global N
global EQUITY
global D
global R
global T

N = 0
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
    # change the range of nd2 to avoid the value of 1-nd2 out of the range
    # in the nx-x file
    if 0.000005 < nd2 < 0.5 :
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

def usage():
    print "python kmv3.py -i data/stock-price.data"

def get_input_file():
    opts, args = getopt.getopt(sys.argv[1:], "hi:o:")
    input_file=""
    output_file=""
    for op, value in opts:
        if op == "-i":
            input_file = value
        elif op == "-o":
            output_file = value
        elif op == "-h":
            usage()
            sys.exit()
    return input_file

if __name__=="__main__":
    main()
