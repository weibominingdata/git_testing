# read input data, content stored, extracted chr, startpos, endpos
# read godstd, content stored, use chr1 as key, use a list with start, end, cnv type as value

import sys

if __name__ == "__main__":
    if (len(sys.argv) == 2):
        fileA = sys.argv[1]
    else:
        print 'Please use extract_del_human input > output'
        exit(1)
    # load input data
    lineNum = 0
    for line in open(fileA, 'r'):
        line = line.rstrip("\r")
        line = line.rstrip("\n")
        if (lineNum == 0):
            lineNum = lineNum+1
            print line
            continue
        else:
            record = []
            posInfo = []    
            chr, str, stp, state, cn, sample, score, n = line.split("\t")
            if int(state)<2:
                print line

                         
            
    
    
        
