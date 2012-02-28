# read input data, content stored, extracted chr, startpos, endpos
# read godstd, content stored, use chr1 as key, use a list with start, end, cnv type as value

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
    if (len(sys.argv) == 4):
        fileA = sys.argv[1]
        fileB = sys.argv[2]
        fileC = sys.argv[3]
    else:
        print 'Please use calculateSensitivity inputdata goldstd inputdatawithoverlappinginformation> statistics'
        exit(1)
    NORMAL = 2
    # load input data
    CHR = ""
    contentA = []
    lineNum = 0
    for line in open(fileA, 'r'):
        if (lineNum == 0):
            lineNum = lineNum+1
            continue
        else:
            record = []
            posInfo = []    
            chr, str, stp, state, cn, sample, score, n = line.split("\t")
            CHR = "chr"+chr
            record.append(CHR)
            posInfo.append(int(str))
            posInfo.append(int(stp))
            record.append(posInfo)
            record.append(int(state))
            record.append(0) # amount of correct overlapping
            record.append(0) # amount of overlapping
            record.append(score)
            record.append(chr)
            record.append(int(n))
            record.append(0)              # if overlapping with a segment in the gold standard, here is the start pos of the gold stardard
            record.append(0)              # end pos of the segment in the gold standard
            record.append("NON")             # type of the segment in the gold standard
            contentA.append(record)
            lineNum = lineNum+1
    # load goldstd data
    contentB = []
    for line in open(fileB, 'r'):
        line = line.rstrip('\n')
        line = line.rstrip('\r')        
        
        record = []
        posInfo = []
        chr, str, stp, type = line.split("\t")
        record.append(chr)
        posInfo.append(int(str))
        posInfo.append(int(stp))
        record.append(posInfo)
        record.append(type)
        record.append([0 for x in xrange(int(stp)-int(str)+1)]) # amount of correct overlapping
        record.append([0 for x in xrange(int(stp)-int(str)+1)]) # amount of overlapping
        contentB.append(record)
    
#    print CHR
#    totalCNVBPS = 0
   
#    for y in contentB:
#        if y[0] == CHR:
#            totalCNVBPS = totalCNVBPS + y[1][1]-y[1][0]+1
            
#    print totalCNVBPS

           
            
#    correctDetectedCNVBPS = 0    
    totalOverlap = 0       
    for x in contentA:
        for y in contentB:
            if x[0]==y[0]:
                if aOverlapB(x[1],y[1]):
                    totalOverlap = totalOverlap + 1
                    overlap = aOverlapInB(x[1],y[1])
                    if (y[2]=="DUP" and x[2]>NORMAL) or (y[2]=="DEL" and x[2]<NORMAL):
                        x[3] = x[3] + overlap
                        l,r = intersects(x[1],y[1])
                        lIndex = l-y[1][0]
                        lr = r-l+1
                        for m in xrange(lr):
                            if y[3][lIndex+m]==0:
                                y[3][lIndex+m] = 1                                
                    x[4] = x[4] + overlap
                    x[8] = y[1][0]
                    x[9] = y[1][1]
                    x[10] = y[2]
                    l,r = intersects(x[1],y[1])
                    lIndex = l-y[1][0]
                    lr = r-l+1
                    for m in xrange(lr):
                        if y[4][lIndex+m]==0:
                            y[4][lIndex+m] = 1                                


    #output the new detected segments with overlapping information
    f = open(fileC, 'w')
    header = ("chr\tstart\tend\tstate\tcn\tsample\tscore\tn\toverlapping\tgstart\tgend\tgtype\tmscore\n")
    f.write(header)
    for x in contentA:
        record = ("%s\t%d\t%d\t%d\tcn\tsample\t%s\t%d\t")%(x[6],x[1][0],x[1][1],x[2],x[5],x[7])
        if x[3] > 0:
            record = record+"1"
        else:
            record = record+"0"
        record = record + ("\t%d\t%d\t%s\t%f\n")%(x[8],x[9],x[10],float(x[5])/x[7])
        f.write(record)
    f.close()
                    
                    
    print totalOverlap                
                        
    nCNVsegGold = 0 # number of segments in the gold standard
    nCNVbpsGold = 0 # number of bps in the gold standard
    nCNVsegGoldDetectedCorrect = 0 
    nCNVsegGoldDetected = 0
    nCNVbpsGoldDetectedCorrect = 0
    nCNVbpsGoldDetected = 0
    
    
    goldStandardDetected = []
    
    
    index = 0
    for y in contentB:
        index = index+1
        if y[0] == CHR:
            nCNVsegGold = nCNVsegGold + 1
            bps = y[1][1]-y[1][0]+1
            nCNVbpsGold = nCNVbpsGold + bps
            if (sum(y[3]) >= bps*0.5):
                nCNVsegGoldDetectedCorrect = nCNVsegGoldDetectedCorrect + 1
            if (sum(y[4]) >= bps*0.5):
                nCNVsegGoldDetected = nCNVsegGoldDetected + 1
            nCNVbpsGoldDetectedCorrect =  nCNVbpsGoldDetectedCorrect+sum(y[3])
            nCNVbpsGoldDetected = nCNVbpsGoldDetected + sum(y[4])
            detectSituation = [y,4,0]
            if sum(y[4]) == 0:
                detectSituation[1] = 0
            elif sum(y[3]) == 0:
                detectSituation[1] = 1
            elif sum(y[4]) < bps*0.5:
                detectSituation[1] = 2
            elif sum(y[3]) < bps*0.5:
                detectSituation[1] = 3
            if sum(y[4]) >= bps*0.5:
                detectSituation[2] = 1
            goldStandardDetected.append(detectSituation)                        

    # ad-hoc way to solve the division by 0 problem            
    if nCNVsegGold ==0:
        nCNVsegGold = 1
    if nCNVbpsGold == 0:
        nCNVbpsGold = 1
            
                        
    print "sensitivity"
    print "Total number of segments in gold standard is %d, the total number of bps is %d"%(nCNVsegGold, nCNVbpsGold)
    print "Correct detected segments are %d, the proportion is %f"%(nCNVsegGoldDetectedCorrect, float(nCNVsegGoldDetectedCorrect)/nCNVsegGold)
    print "Correct detected bps are %d, the proportion is %f"%(nCNVbpsGoldDetectedCorrect, float(nCNVbpsGoldDetectedCorrect)/nCNVbpsGold)
#    print "Detected segments are %d, the proportion is %f"%(nCNVsegGoldDetected, float(nCNVsegGoldDetected)/nCNVsegGold)
#    print "Detected bps are %d, the proportion is %f"%(nCNVbpsGoldDetected, float(nCNVbpsGoldDetected)/nCNVbpsGold)
    
    nCNVsegInfer = 0  # number of segments in the detection set
    nCNVbpsInfer = 0  # number of bps in the detection set
    nCNVsegInferDetectedCorrect = 0 # number of correct segments in the detection set
    nCNVsegInferDetected = 0             
    nCNVbpsInferDetectedCorrect = 0 # number of correct bps in the detection set
    nCNVbpsInferDetected = 0
    
    #revised by Weibo
    nCNVsegInferDel = 0
    nCNVbpsInferDel = 0
    nCNVsegCorrectInferDel = 0
    nCNVbpsCorrectInferDel = 0

    nCNVsegInferDup = 0
    nCNVbpsInferDup = 0
    nCNVsegCorrectInferDup = 0
    nCNVbpsCorrectInferDup = 0
    

    for x in contentA:
        nCNVsegInfer = nCNVsegInfer + 1
        bps = x[1][1]-x[1][0]+1
        nCNVbpsInfer = nCNVbpsInfer + bps
        if x[2] < NORMAL:
            nCNVsegInferDel = nCNVsegInferDel + 1
            nCNVbpsInferDel = nCNVbpsInferDel + bps
        else:
            nCNVsegInferDup = nCNVsegInferDup + 1
            nCNVbpsInferDup = nCNVbpsInferDup + bps
        if (x[3] >= bps*0.5):
            nCNVsegInferDetectedCorrect = nCNVsegInferDetectedCorrect + 1
            nCNVbpsInferDetectedCorrect =  nCNVbpsInferDetectedCorrect+x[3]
            if x[2] < NORMAL:
                nCNVsegCorrectInferDel = nCNVsegCorrectInferDel + 1
                nCNVbpsCorrectInferDel = nCNVbpsCorrectInferDel + x[3]
            else:
                nCNVsegCorrectInferDup = nCNVsegCorrectInferDup + 1
                nCNVbpsCorrectInferDup = nCNVbpsCorrectInferDup + x[3]

#        if (x[4] >= bps*0.5):
#            nCNVsegInferDetected = nCNVsegInferDetected + 1
#        
#        nCNVbpsInferDetected = nCNVbpsInferDetected + x[4]      

    if nCNVsegInfer == 0:
        nCNVsegInfer = 1
    if nCNVbpsInfer == 0:
        nCNVbpsInfer = 1

    print "specificity"        
    print "Total number of segments in detection is %d, the total number of bps is %d"%(nCNVsegInfer, nCNVbpsInfer)
    print "Correct overlapping segments are %d, the proportion is %f"%(nCNVsegInferDetectedCorrect, float(nCNVsegInferDetectedCorrect)/nCNVsegInfer)
    print "Correct overlapping bps are %d, the proportion is %f"%(nCNVbpsInferDetectedCorrect, float(nCNVbpsInferDetectedCorrect)/nCNVbpsInfer)
#    print "Overlapping segments are %d, the proportion is %f"%(nCNVsegInferDetected, float(nCNVsegInferDetected)/nCNVsegInfer)
#    print "Overlapping bps are %d, the proportion is %f"%(nCNVbpsInferDetected, float(nCNVbpsInferDetected)/nCNVbpsInfer)
    
    
    #output number of each detected states, in bp
    stateNum = [0 for x in xrange(7)]
    for x in contentA:
        stateNum[x[2]] = stateNum[x[2]] + x[1][1]-x[1][0]+1
    
    for x in xrange(len(stateNum)):
        print "state %d : %d bps are detected"%(x,stateNum[x])
        
    
    for x in goldStandardDetected:
        print "%s\t%d\t%d\t%s\t%d"%(x[0][0],x[0][1][0], x[0][1][1], x[0][2],x[1])
        
        
    #output sensitivity on duplication and deletion
    nCNVdup = 0
    nCNVdel = 0
    nCNVdupcorrect = 0
    nCNVdelcorrect = 0
    
    bpsCNVdup = 0
    bpsCNVdel = 0
    bpsCNVdupcorrect = 0
    bpsCNVdelcorrect = 0
    
    index = 0
    for y in contentB:
        index = index+1
        if y[0] == CHR:
            bps = y[1][1]-y[1][0]+1
            if y[2] == "DUP":
                nCNVdup = nCNVdup+1
                if (sum(y[3]) >= bps*0.5):
                    nCNVdupcorrect = nCNVdupcorrect+1
                bpsCNVdup = bpsCNVdup + bps
                bpsCNVdupcorrect = bpsCNVdupcorrect + sum(y[3])
            elif y[2] == "DEL":
                nCNVdel = nCNVdel+1
                if (sum(y[3]) >= bps*0.5):
                    nCNVdelcorrect = nCNVdelcorrect+1 
                bpsCNVdel = bpsCNVdel + bps
                bpsCNVdelcorrect = bpsCNVdelcorrect + sum(y[3])

    if nCNVdup == 0:
        nCNVdup = 1
    if nCNVdel == 0:
        nCNVdel = 1

    if bpsCNVdup == 0:
        bpsCNVdup = 1
    if bpsCNVdel == 0:
        bpsCNVdel = 1

    print "Sensitivity on DUP and DEL"
    print "There are %d DUP, %d are correctly detected, the ratio is %f"%(nCNVdup, nCNVdupcorrect, float(nCNVdupcorrect)/nCNVdup)               
    print "There are %d DEL, %d are correctly detected, the ratio is %f"%(nCNVdel, nCNVdelcorrect, float(nCNVdelcorrect)/nCNVdel)
    print "There are %d bps DUP, %d bps are correctly detected, the ratio is %f"%(bpsCNVdup, bpsCNVdupcorrect, float(bpsCNVdupcorrect)/bpsCNVdup)               
    print "There are %d bps DEL, %d bps are correctly detected, the ratio is %f"%(bpsCNVdel, bpsCNVdelcorrect, float(bpsCNVdelcorrect)/bpsCNVdel)

    if nCNVsegInferDel == 0:
        nCNVsegInferDel = 1
    if nCNVbpsInferDel == 0:
        nCNVbpsInferDel = 1
    if nCNVsegInferDup == 0:
        nCNVsegInferDup = 1
    if nCNVbpsInferDup == 0:
        nCNVbpsInferDup = 1
    
          

    filewholegenome = open("wholegenome.txt",'a')
    #write sensitivity overall
    filewholegenome.write("%s\t%f\t%d\t%d\t%f\t%d\t%d\t"%(fileC,float(nCNVsegGoldDetectedCorrect)/nCNVsegGold,nCNVsegGoldDetectedCorrect,nCNVsegGold,float(nCNVbpsGoldDetectedCorrect)/nCNVbpsGold,nCNVbpsGoldDetectedCorrect,nCNVbpsGold))
    #write sensitivity straitified by del and dup
    filewholegenome.write("%f\t%d\t%d\t%f\t%d\t%d\t%f\t%d\t%d\t%f\t%d\t%d\t"%(float(nCNVdelcorrect)/nCNVdel, nCNVdel, nCNVdelcorrect, float(bpsCNVdelcorrect)/bpsCNVdel, bpsCNVdel, bpsCNVdelcorrect, float(nCNVdupcorrect)/nCNVdup, nCNVdup, nCNVdupcorrect, float(bpsCNVdupcorrect)/bpsCNVdup, bpsCNVdup, bpsCNVdupcorrect))
    #write specificity overall
    filewholegenome.write("%f\t%d\t%d\t"%(float(nCNVsegInferDetectedCorrect)/nCNVsegInfer, nCNVsegInferDetectedCorrect, nCNVsegInfer))
    filewholegenome.write("%f\t%d\t%d\t"%(float(nCNVbpsInferDetectedCorrect)/nCNVbpsInfer, nCNVbpsInferDetectedCorrect, nCNVbpsInfer))
    #write specificity straitified by del and dup
    filewholegenome.write("\t%f\t%d\t%d\t%f\t%d\t%d\t%f\t%d\t%d\t%f\t%d\t%d\t\n"%(float(nCNVsegCorrectInferDel)/nCNVsegInferDel, nCNVsegCorrectInferDel,nCNVsegInferDel,float(nCNVbpsCorrectInferDel)/nCNVbpsInferDel,nCNVbpsCorrectInferDel,nCNVbpsInferDel,float(nCNVsegCorrectInferDup)/nCNVsegInferDup,nCNVsegCorrectInferDup,nCNVsegInferDup,float(nCNVbpsCorrectInferDup)/nCNVbpsInferDup,nCNVbpsCorrectInferDup,nCNVbpsInferDup))
    filewholegenome.close()
    
    
    
#    print correctDetectedCNVBPS
#    print "specificity is %f"%(float(correctDetectedCNVBPS) / totalCNVBPS)
                    
                         
            
    
    
        
