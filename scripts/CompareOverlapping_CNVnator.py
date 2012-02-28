import sys

def aOverlapB(a, b):
    if (a[0]>a[1] or b[0]>b[1]):
        print "Wrong input"
        return False
    if (a[0] < b[0]):
        if (a[1] < b[0]):
            return False
        else:
            return True
    else:
        if (a[0] > b[1]):
            return False
        else:
            return True
        
def aOverlapInB(a, b):
    if (a[0]>a[1] or b[0]>b[1]):
        print "Wrong input"
        return 0
    if (a[0] < b[0]):
        if (a[1] < b[0]):
            return 0
        else:
            return min(a[1],b[1])-b[0]+1
    else:
        if (a[0] > b[1]):
            return 0
        else:
            return min(a[1],b[1])-a[0]+1  
        
def intersects(a, b):
    if (a[0]>a[1] or b[0]>b[1]):
        print "Wrong input"
        return 0,0
    if (a[0] < b[0]):
        if (a[1] < b[0]):
            return 0,0
        else:
            return b[0], min(a[1],b[1])
    else:
        if (a[0] > b[1]):
            return 0
        else:
            return a[0], min(a[1],b[1])                

if __name__ == "__main__":
    nSAMPLE=2
    if (len(sys.argv) == nSAMPLE+1):
        files = []
        for i in xrange(nSAMPLE):
            files.append(sys.argv[i+1])
    else:
        print 'Please use CompareOverlapping Inferred1 Inferred2'
        exit(1)
    # load input data and statistics the data
    NORMAL = 2
    contents = []
    headers = []
    statistics = []
    for i in xrange(nSAMPLE):
        content = []
        lineNum = 0
        statistic = [0,0,0,0]
        for line in open(files[i], 'r'):
            line = line.rstrip('\n')
            line = line.rstrip('\r')      
            if (lineNum == 0):
                header = line
                lineNum = lineNum+1
                continue
            else:
                record = []
                posInfo = []    
                chr, str, stp, state, cn, sample, score, n = line.split("\t")
                record.append(chr)
                posInfo.append(int(str))
                posInfo.append(int(stp))
                record.append(posInfo)
                record.append(int(state))
                if (int(state)>NORMAL):
                    statistic[0] = statistic[0]+1
                else:
                    statistic[1] = statistic[1]+1
                record.append(cn)
                record.append(sample)
                record.append(score)
                record.append(n)
                record.append(True) #indicating whether this record should be kept
                record.append([1 for x in xrange(int(stp)-int(str)+1)])
                content.append(record)
                lineNum = lineNum+1
        contents.append(content)
        headers.append(header)
        statistics.append(statistic)

    for i in xrange(nSAMPLE):
        for x in contents[i]:
            for j in xrange(nSAMPLE):
                if i!=j:
                    for y in contents[j]:
                        if x[0]!=y[0]:
                            continue
                        if x[1][1] < y[1][0]:
                            continue
                        if not aOverlapB(x[1],y[1]):
                            continue
                        if (x[2]<NORMAL and y[2]<NORMAL) or (x[2]>NORMAL and y[2]>NORMAL): #overlapped, need to know which part are overlapped
                            lb = max(x[1][0],y[1][0]) #left boundary of overlapping
                            rb = min(x[1][1],y[1][1]) #right boundary of overlapping
                            lindex = lb-x[1][0]       #starting affect pos in x
                            length = rb-lb+1          #len of affect regions in x
                            for k in xrange(length):
                                x[8][lindex+k]=x[8][lindex+k]+1

    for i in xrange(nSAMPLE):
        for x in contents[i]:
            size = x[1][1]-x[1][0]+1
            appearInAllNum=0
            for k in xrange(size):
                if x[8][k]>=nSAMPLE:
                    appearInAllNum=appearInAllNum+1
            if float(appearInAllNum) > 0.5*float(size): #should be removed
                x[7] = False
            else: #aggregating the number
                if x[2] > NORMAL:
                    statistics[i][2]=statistics[i][2]+1
                else:
                    statistics[i][3]=statistics[i][3]+1
                        
            
#    for i in xrange(6):
#        fileName = open("%s_commonCNV_removed.txt"%(files[i]),'w')
#        fileName.write("%s\n"%(headers[i]))
#        for x in contents[i]:
#            if x[7] == True:
#                fileName.write("%s\t%d\t%d\t%d\t%s\t%s\t%s\t%s\n"%(x[0],x[1][0],x[1][1],x[2],x[3],x[4],x[5],x[6]))
#        fileName.close()

            
    fileStat = open("Stat.txt",'a')
    for i in xrange(nSAMPLE):
#        fileStat.write("%s\n"%(files[i]))
#        fileStat.write("%d Dup CNV callings before filtering\n"%(statistics[i][0]))
#        fileStat.write("%d Del CNV callings before filtering\n"%(statistics[i][1]))
#        fileStat.write("%d Dup CNV callings after filtering, the FDR is %f\n"%(statistics[i][2], float(statistics[i][0]-statistics[i][2])/statistics[i][0]))
#        fileStat.write("%d Del CNV callings after filtering, the FDR is %f\n"%(statistics[i][3], float(statistics[i][1]-statistics[i][3])/statistics[i][1]))
        fileStat.write("%s\t"%(files[i]))
        fileStat.write("%d\t"%(statistics[i][0]))
        fileStat.write("%d\t"%(statistics[i][1]))
        fileStat.write("%d\t%f\t"%(statistics[i][2], float(statistics[i][0]-statistics[i][2])/statistics[i][0]))
        fileStat.write("%d\t%f\t"%(statistics[i][3], float(statistics[i][1]-statistics[i][3])/statistics[i][1]))

    fileStat.write("\n")
    fileStat.close()
        
