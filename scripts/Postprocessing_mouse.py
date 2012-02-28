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
    if (len(sys.argv) == 2):
        fileChild = sys.argv[1]
    else:
        print 'Please use Postprocessing childInferredResult > childFilterredResult'
        exit(1)
    # load input data and statistics the data
    NORMAL=1
    nDup = 0
    nDel = 0
    contentChild = []
    lineNum = 0
    for line in open(fileChild, 'r'):
        line = line.rstrip('\n')
        line = line.rstrip('\r')      
        if (lineNum == 0):
            print line
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
            if (int(state)<NORMAL):
                nDel = nDel+1
            else:
                nDup = nDup+1
            record.append(cn)
            record.append(sample)
            record.append(score)
            record.append(n)
            contentChild.append(record)
            lineNum = lineNum+1

    nDupRemaining = 0
    nDelRemaining = 0
    # step removing
    contentChildAfterRemoving = []
    for x in contentChild:
        if (int(x[6])>1 and float(x[5])/int(x[6]) > 0.5):
            if (x[2]>NORMAL):
                nDupRemaining = nDupRemaining+1
            else:
                nDelRemaining = nDelRemaining+1
            contentChildAfterRemoving.append(x)

    nDupRemaining = 0
    nDelRemaining = 0
    # step merging
    contentChildAfterMerging = []
    index = 0
    while index < len(contentChildAfterRemoving):
        current = contentChildAfterRemoving[index]
        pivot = index+1
        while pivot < len(contentChildAfterRemoving):
            c = contentChildAfterRemoving[pivot]
            if ((c[2]<NORMAL and current[2]<NORMAL) or (c[2]>NORMAL and current[2]>NORMAL)):
                if (2*(c[1][0]-current[1][1]) < (c[1][1]-c[1][0]+current[1][1]-current[1][0])
                    and (c[1][0]-current[1][1]) < min(c[1][1]-c[1][0],current[1][1]-current[1][0])):
                    #can be merged, however, after merge, only chr, type, and pos are accurate
                    current[1][1] = c[1][1]
                    pivot=pivot+1
                else:
                    break
            else:
                break
        contentChildAfterMerging.append(current)
        index = pivot
        if (current[2]>2):
            nDupRemaining = nDupRemaining+1
        else:
            nDelRemaining = nDelRemaining+1
                    

    #print "%d %d %d %d"%(nDel,nDup,nDelRemaining,nDupRemaining)
    for x in contentChildAfterMerging:
        print "%s\t%d\t%d\t%d\t%s\t%s\t%s\t%s"%(x[0],x[1][0],x[1][1],x[2],x[3],x[4],x[5],x[6])



    
            
##    contentParent1 = []
##    contentParent2 = []
##    
##    lineNum = 0
##    for line in open(filePARENT1, 'r'):
##        line = line.rstrip('\n')
##        line = line.rstrip('\r')     
##        if (lineNum == 0):
##            lineNum = lineNum+1
##            continue
##        else:
##            record = []
##            posInfo = []    
##            chr, str, stp, state, cn, sample, score, n = line.split("\t")
##            record.append(chr)
##            posInfo.append(int(str))
##            posInfo.append(int(stp))
##            record.append(posInfo)
##            record.append(int(state))
##            record.append(cn)
##            record.append(sample)
##            record.append(score)
##            record.append(n)
##            contentParent1.append(record)
##            lineNum = lineNum+1
##            
##    lineNum = 0
##    for line in open(filePARENT2, 'r'):
##        line = line.rstrip('\n')
##        line = line.rstrip('\r')     
##        if (lineNum == 0):
##            lineNum = lineNum+1
##            continue
##        else:
##            record = []
##            posInfo = []    
##            chr, str, stp, state, cn, sample, score, n = line.split("\t")
##            record.append(chr)
##            posInfo.append(int(str))
##            posInfo.append(int(stp))
##            record.append(posInfo)
##            record.append(int(state))
##            record.append(cn)
##            record.append(sample)
##            record.append(score)
##            record.append(n)
##            contentParent2.append(record)
##            lineNum = lineNum+1            
##    
##    for i in xrange(len(contentChild)):
##        x = contentChild[i]
##        index = -1
##        for y in contentParent1:
##            index = index+1
##            if (x[0]==y[0]):
##                if ((x[2]>2 and y[2]>2) or (x[2]<2 and y[2]<2)):
##                    if (aOverlapInB(x[1],y[1]) > 0.5*(x[1][1]-x[1][0])):
##                        contentChild[i][7]="TRUE"
##                        contentChild[i][8]=index
##                    
##    for i in xrange(len(contentChild)):
##        index = -1
##        x = contentChild[i]
##        for y in contentParent2:
##            index = index+1
##            if (x[0]==y[0]):
##                if ((x[2]>2 and y[2]>2) or (x[2]<2 and y[2]<2)):
##                    if (aOverlapInB(x[1],y[1]) > 0.5*(x[1][1]-x[1][0])):
##                        contentChild[i][7]="TRUE"
##                        contentChild[i][9]=index
##                   
##    nDupRemaining = 0
##    nDelRemaining = 0
##    
##    for x in contentChild:
##        print "%s\t%s\t%d\t%d\t%d\t%s\t%s\t%s\t%s"%("NA12878",x[0],x[1][0],x[1][1],x[2],x[3],x[4],x[5],x[6])               
##        if (x[7]=="TRUE"):
##            if (x[2] > 2):
##                nDupRemaining = nDupRemaining + 1
##            else:
##                nDelRemaining = nDelRemaining + 1
##            ##print "%s\t%s\t%d\t%d\t%d\t%s\t%s\t%s\t%s"%("NA12878",x[0],x[1][0],x[1][1],x[2],x[3],x[4],x[5],x[6])               
##            if x[8] != -1:
##                y = contentParent1[x[8]]
##                print "%s\t%s\t%d\t%d\t%d\t%s\t%s\t%s\t%s"%("NA12891",y[0],y[1][0],y[1][1],y[2],y[3],y[4],y[5],y[6])       
##            if x[9] != -1:
##                y = contentParent2[x[9]]
##                print "%s\t%s\t%d\t%d\t%d\t%s\t%s\t%s\t%s"%("NA12892",y[0],y[1][0],y[1][1],y[2],y[3],y[4],y[5],y[6])              
##            
##    fileStat = open("Stat.txt",'w')
##    fileStat.write("%d Dup CNV callings before filtering\n"%(nDup))
##    fileStat.write("%d Del CNV callings before filtering\n"%(nDel))
##    fileStat.write("%d Dup CNV callings after filtering, the FDR is %f\n"%(nDupRemaining, float(nDup-nDupRemaining)/nDup))
##    fileStat.write("%d Del CNV callings after filtering, the FDR is %f\n"%(nDelRemaining, float(nDel-nDelRemaining)/nDel))
##    
##    fileStat.close()
        
