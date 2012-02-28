import sys
import csv
import os.path

SENSITIVITY=1
SPECIFICITY=2

def collectingData(path,datatype=SENSITIVITY):
    collectedData = [0,0,0,0]
    data = csv.reader(open(path, 'rb'), delimiter='\t')
    for row in data:
        if datatype==SENSITIVITY:
            rowData=[int(row[8]),int(row[9]),int(row[14]),int(row[15])]
        elif datatype==SPECIFICITY:
            rowData=[int(row[0]),int(row[1]),int(row[2]),int(row[3])]
        else:
            rowData = [0,0,0,0] # #gold in del #overlapped in del #gold in dup #overlapped in dup
        collectedData=[collectedData[i]+rowData[i] for i in xrange(len(collectedData))]
    collectedData[0] = max(1,collectedData[0])
    collectedData[2] = max(1,collectedData[2])
    if datatype==SENSITIVITY:
        ratio=[float(collectedData[1])/collectedData[0],float(collectedData[3])/collectedData[2]]
    elif datatype==SPECIFICITY:
        ratio=[float(collectedData[0]-collectedData[1])/collectedData[0],float(collectedData[2]-collectedData[3])/collectedData[2]]
    else:
        ratio=[0,0]
    return (collectedData, ratio)

def outputData(path, data, ratio):
    #path is used to identify which data is analyzed
    # data must be int, ratio must float between [0,1]
    sys.stdout.write(path+"\t")
    for d in data:
        sys.stdout.write("%d\t"%(d))
    for r in ratio:
        sys.stdout.write("%f\t"%(r))
    sys.stdout.write("\n")
        

if __name__ == "__main__":
    # useage should be collectingData path type
    if (len(sys.argv)==3):
        path = sys.argv[1]
        type = sys.argv[2]
    else:
        print "Usage: collectingData path type"
        
    #checking the input
    if not os.path.exists(path):    
        print "path not exist"
        exit()
    if not type.isdigit():
        print "type should be a number"
        exit()
    type=int(type)
    print type
    if type != SENSITIVITY and type != SPECIFICITY:
        print "type the known type"
        exit()
    
    # collecting data
    collectedData, ratio = collectingData(path, type)
    
    #output
    outputData(path, collectedData, ratio)
    