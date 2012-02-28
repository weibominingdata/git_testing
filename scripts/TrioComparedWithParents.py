# pure test~~~~


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
        
def parsingLine(line, format):
    if format==1:
        record = []
        posInfo = []    
        chr, str, stp, state, cn, sample, score, n = line.split("\t")
        record.append(chr)
        posInfo.append(int(str))
        posInfo.append(int(stp))
        record.append(posInfo)
        record.append(int(state))
        record.append(cn)
        record.append(sample)
        record.append(score)
        record.append(n)
        record.append("FALSE") #indicating whether this record should be kept   
        return (record,state)
    if format==2:
        record = []
        posInfo = []    
        type, chrpos, n, a, b, c, d, e, f = line.split("\t")
        chr, pos = chrpos.split(":")
        str, stp = pos.split("-");
        record.append(chr)
        posInfo.append(int(str))
        posInfo.append(int(stp))
        record.append(posInfo)
        if type == "deletion":
            state="0"
        else:
            state="4"
        record.append(int(state))        
        record.append("cn")
        record.append("sample")
        record.append("score")
        record.append("n")
        record.append("FALSE") #indicating whether this record should be kept   
        return (record,state)
             

if __name__ == "__main__":
    if (len(sys.argv) == 5):
        fileChild = sys.argv[1]
        filePARENT1 = sys.argv[2]
        filePARENT2 = sys.argv[3]
        fileType = int(sys.argv[4])
    else:
        print 'Please use TrioPairComparison Genome1Result Genome2Result Genome3Result resultType(1 our, 2 cnvnator)'
        exit(1)
    # load input data and statistics the data
    nDup = 0
    nDel = 0
    contentChild = []
    lineNum = 0
    for line in open(fileChild, 'r'):
        line = line.rstrip('\n')
        line = line.rstrip('\r')      
        if (lineNum == 0):
            #print line
            lineNum = lineNum+1
            continue
        else:
            record,state = parsingLine(line,fileType)
            if (int(state)<2):
                nDel = nDel+1
            else:
                nDup = nDup+1
            contentChild.append(record)
            lineNum = lineNum+1
            
    contentParent1 = []
    contentParent2 = []
    
    lineNum = 0
    for line in open(filePARENT1, 'r'):
        if (lineNum == 0):
            lineNum = lineNum+1
            continue
        else:
            record,state = parsingLine(line,fileType)
            contentParent1.append(record)
            lineNum = lineNum+1

    lineNum = 0
    for line in open(filePARENT2, 'r'):
        if (lineNum == 0):
            lineNum = lineNum+1
            continue
        else:
            record,state = parsingLine(line,fileType)
            contentParent2.append(record)
            lineNum = lineNum+1


            
    for i in xrange(len(contentChild)):
        x = contentChild[i]
        for y in contentParent1:
            if (x[0]==y[0]):
                if ((x[2]>2 and y[2]>2) or (x[2]<2 and y[2]<2)):
                    if (aOverlapInB(x[1],y[1]) >= 0.5*(x[1][1]-x[1][0])):
                        contentChild[i][7]="TRUE"

    for i in xrange(len(contentChild)):
        x = contentChild[i]
        for y in contentParent2:
            if (x[0]==y[0]):
                if ((x[2]>2 and y[2]>2) or (x[2]<2 and y[2]<2)):
                    if (aOverlapInB(x[1],y[1]) >= 0.5*(x[1][1]-x[1][0])):
                        contentChild[i][7]="TRUE"
                    
                   
    nDupRemaining = 0
    nDelRemaining = 0
    
    for x in contentChild:
        if (x[7]=="TRUE"):
            if (x[2] > 2):
                nDupRemaining = nDupRemaining + 1
            else:
                nDelRemaining = nDelRemaining + 1
            #print "%s\t%d\t%d\t%d\t%s\t%s\t%s\t%s"%(x[0],x[1][0],x[1][1],x[2],x[3],x[4],x[5],x[6])               
            

    if nDup == 0:
        nDup = 1
    if nDel == 0:
        nDel = 1
    
    fileStat = open("StatTrio.txt",'a')
    fileStat.write("%d\t%d\t%d\t%d\n"%(nDel,nDelRemaining,nDup,nDupRemaining))
#    fileStat.write("%s\t%s\t%s\t%f\t%f\n"%(sys.argv[1],sys.argv[2],sys.argv[3],float(nDup-nDupRemaining)/nDup,float(nDel-nDelRemaining)/nDel))
#    fileStat.write("%s %s\n"%(sys.argv[1],sys.argv[2]))
#    fileStat.write("%d Dup CNV callings before filtering\n"%(nDup))
#    fileStat.write("%d Del CNV callings before filtering\n"%(nDel))
#    fileStat.write("%d Dup CNV callings after filtering, the FDR is %f\n"%(nDupRemaining, float(nDup-nDupRemaining)/nDup))
#    fileStat.write("%d Del CNV callings after filtering, the FDR is %f\n"%(nDelRemaining, float(nDel-nDelRemaining)/nDel))
    
    fileStat.close()
        
