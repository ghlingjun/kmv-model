# -*- coding: utf-8 -*-
import commons
import math

def get_fd1(sigmaP, sigmaVi, nd1, d1, nd2):
    temp = math.log((commons.EQUITY + (commons.D * math.pow(math.e, -commons.R * commons.T) * nd2) / (nd1 * commons.D)))
    numerator = temp + (commons.R + 0.5 * sigmaVi * sigmaVi) * commons.T
    denominator = sigmaVi * math.sqrt(commons.T)
    fund1i = (d1 - numerator / denominator)
    if fund1i < 0 :
        fund1i = -fund1i
    # print fund1i
    return fund1i

def get_v2(sigmaV, nd1, nd2):
    numerator = commons.D * math.pow(math.e, -commons.R * commons.T) * nd2 + commons.EQUITY
    denominator = nd1
    return numerator / denominator

def main():
    input_file = commons.get_input_file()
    data_file = "stock-price.data"
    out_file = "out.data"
    outputfile = open(out_file, "w")
    outputfile.write(time.localtime() + "method 1")
    if input_file != "" :
        inputfile = open(input_file, "r")
        while True :
            line = inputfile.readline()
            if not line :
                break
            outputfile.write(line)
            list_values = line.split(',')
            print line.split(',')
            commons.R = float(list_values[0])
            commons.D = float(list_values[1])
            commons.EQUITY = float(list_values[2])
            data_file = list_values[3].rstrip()
            # read price of stock from file "stock-price.data"
            listP = commons.get_listP(data_file)
            commons.N = len(listP)
            sigmaP = commons.get_sigmaP(listP)
            # print "The volatility of the stock's price: sigmaP = %10.12f" % sigmaP
            sigmaVi = sigmaV0 = commons.get_sigmaV0(sigmaP) # sigmaV0 is the down limit
            # print sigmaV0
            sigmaV = nd1 = 0.0
            fund1 = 99999
            while True :
                sigmaVi += 0.0001
                if sigmaVi > sigmaP :
                    break
                nd2i = commons.get_nd2(sigmaP, sigmaVi)
                d2i = commons.get_d2(nd2i, "nx-x")
                if d2i == 9999 :
                    continue
                d1i = sigmaVi * commons.T + d2i
                nd1i = commons.get_nd1(d1i, "x-nx")
                fund1i = get_fd1(sigmaP, sigmaVi, nd1i, d1i, nd2i)
                if fund1 > fund1i :
                    fund1 = fund1i
                    sigmaV = sigmaVi
                    nd1 = nd1i
            v = get_v2(sigmaP, nd1, sigmaV)
            dd = (v - commons.D) / (v * sigmaV)
            print "DD is %.10f" % dd
            outputfile.write("DD is %.10f" % dd)
            edf = commons.get_nd1(-dd, "x-nx")
            print "EDF is %.10f\n" % edf
            outputfile.write("EDF is %.10f\n" % edf)
        inputfile.close()
    outputfile.close()

if __name__=="__main__":
    main()
