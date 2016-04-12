from __future__ import print_function
import csv
import copy
import time 

dataPath = '/home/aeon/Proj2/GSP/DATASET6.csv'
configPath = '/home/aeon/Proj2/GSP/Parameters6.config'

def main():
    seqSet = getSeq()
    minSup = getParam()
    start = time.clock()
    freqSequences = PrefixSpan(seqSet,minSup)
    end = time.clock()
    print("\nFrequent Sequences \n-------------------")
    print("\nNo of Sequences Found : "+str(len(freqSequences)))
    for sequence in freqSequences:
        count = len(sequence)
        print("")
        for elem in sequence:
            #print("Printing Element"+str(elem)+"with index: "+str(sequence.index(elem)))
            for item in elem:
                print(item,end="")
                #print("Printing item "+item)
            count -= 1
            if count > 0:
                print(",",end="")
    print("\nTime Taken : "+str(end - start))

def PrefixSpan(seqSet,minSup):
    freqSequences = []
    curPrefixes = []
    curFreqPrefixes = []
    k = 1
    #Finding Length 1 Frequent Prefixes
    for sequence in seqSet:
        for element in sequence:
            for item in element:
                if [[item]] not in curPrefixes :
                    curPrefixes.append([[item]])
    #print ("\n1 Length Prefixes : " + str(curPrefixes))
    for prefix in curPrefixes:
        if findItemSupport(prefix[0][0],seqSet) >= minSup:
            curFreqPrefixes.append(prefix)
    curFreqPrefixes.sort()
    #print ("\n1 Frequent Prefixes : " + str(curFreqPrefixes))
    freqSequences.append(curFreqPrefixes)
    for prefix in curFreqPrefixes:
        projectionDB = findProjectionDB(prefix,seqSet)
        #print ("\n "+str(prefix)+" ProjectionDB : "+str(projectionDB))        
        curPrefixes = []
        prefixSpanRecursion(prefix,projectionDB,curPrefixes,seqSet,minSup)
        #print("\nCurPrefixes : "+str(curPrefixes))
        for pre in curPrefixes:
            if pre not in curFreqPrefixes:
                curFreqPrefixes.append(pre)
        curFreqPrefixes.sort()
    return curFreqPrefixes

def prefixSpanRecursion(prefix,projectionDB,curPrefixes,seqSet,minSup):
    if len(projectionDB) < minSup:
        return
    curFreqPrefixes = []
    [itemList,countList] = findPrefixes(projectionDB,prefix)
    #print ("\nItemlist : "+str(itemList)+"\nCountList : "+str(countList))
    #print("\nPrefix : "+str(prefix))
    for i in range(0,len(itemList)):
        if countList[i] >= minSup:
            #curFreqPrefixes.append(prefixList[index])
            newprefix  = copy.deepcopy(prefix)
            #print(newprefix)
            if '_' in itemList[i]:
                newprefix[len(newprefix) - 1].append(itemList[i][1])
            else:
                newprefix.append(itemList[i])
            #print("\nadding item "+ str(newprefix))
            curFreqPrefixes.append(newprefix)                
    #print ("\nCurrent FreqPrefixes: "+str(curFreqPrefixes))
    for prefix in curFreqPrefixes:
        if  not prefix in curPrefixes:
            curPrefixes.append(prefix)
            newProjDB = findProjectionDB(prefix,seqSet)
            #print ("\n"+str(prefix)+" Projected DB : "+str(newProjDB))
            prefixSpanRecursion(prefix,newProjDB,curPrefixes,seqSet,minSup)
            
def compareElems(element1,element2):
    count = len(element1)
    for item in element1:
        if item in element2:
            count -= 1
    if count == 0:
        return True
    return False
        
def findPrefixes(projectionDB,prefix):
    countList = []
    itemList = []
    #print("\nFinding Prefixes for "+str(prefix))
    for sequence in projectionDB:
        #print("\nTaking Sequence"+str(sequence))
        if '_' in sequence[0]:
            #print("\n Balance Found")
            if ['_',sequence[0][1]] in itemList:
                #print ("\n Preifx "+str(['_',sequence[0][1]])+" Found" )
                countList[itemList.index(['_',sequence[0][1]])] += 1
            else:
                findPrefix = copy.deepcopy(prefix)
                findPrefix[len(findPrefix) - 1].append(sequence[0][1])
                #print ("\n Prefix to check for is "+str(findPrefix))
                findElem = findPrefix[len(findPrefix) - 1]
                #print("\nChecking for findElem :"+str(findElem))
                support = 1
                for seq in projectionDB:
                    for elem in seq:
                        flag = True
                        for item in findElem:
                            if item not in elem:
                                flag = False
                                break
                        if flag :
                            support += 1
                            break
                itemList.append(['_',sequence[0][1]])
                countList.append(support)
                #print ("\nSupport for"+str(findPrefix)+"is "+str(support))
            repeatList = []
            for i in range(1, len(sequence)):
                for item in sequence[i]:
                    #print("\nItem Found "+ str(item))
                    if [item] not in repeatList:
                        repeatList.append([item])
                        if [item] in itemList:
                            #print ("\nItem in itemList,Incrementing")
                            countList[itemList.index([item])] += 1
                        else:
                            #print("\nItem not in itemList, adding item")
                            itemList.append([item])
                            countList.append(1)
        else:
            repeatList = []
            for element in sequence:
                for item in element:
                    #print("\nItem Found "+ str(item))
                    if [item] not in repeatList:
                        repeatList.append([item])
                        if [item] in itemList:
                            #print ("\nItem in itemList,Incrementing")
                            countList[itemList.index([item])] += 1
                        else:
                            #print("\nItem not in itemList, adding item")
                            itemList.append([item])
                            countList.append(1)
    return [itemList,countList]

    
def findProjectionDB(prefix,seqSet):
    projectionDB = []
    #print("\nFinding ProjectionDB for : "+str(prefix))
    for sequence in seqSet:
        #print("\nFinding Projection of : "+str(sequence))
        elemIndex = 0
        projection = []
        lastItemIndex = -1
        prefixFound = True
        seqLength = len(sequence)
        for elem in prefix:
            #print ("\nChecking if "+str(elem)+" is present")
            elemFound = False
            while elemIndex < seqLength :
                if set(elem).issubset(set(sequence[elemIndex])):
                    #print("\nElement "+str(elem)+" Found in Sequence element : "+str(sequence[elemIndex]))
                    elemFound = True
                    elemIndex += 1
                    break
                else:
                    #print("\nElement not found, Incrementing elemIndex")
                    elemIndex += 1
            if not elemFound:
                #print("\nElement not found in entire sequence,setting prefixFound as False")
                prefixFound = False
                break
        if prefixFound :
            #print("\nEntire Prefix found in Sequence ") 
            elemIndex -= 1
            #print("\nLast Element Index :"+str(elemIndex))
            lastElem = prefix[len(prefix) - 1]
            lastItem = lastElem[len(lastElem) - 1]
            lastItemIndex = sequence[elemIndex].index(lastItem)
            balElement = [] 
            for index in range(lastItemIndex + 1,len(sequence[elemIndex])):
                balElement.append(sequence[elemIndex][index])
            if balElement:
                balElement.insert(0,'_')
                #print("\nBalance items present : "+str(balElement))
                projection.append(balElement)
            elemIndex += 1
            #print ("\nElemIndex:"+str(elemIndex)+" SequenceLength:"+str(seqLength))
            for index in range(elemIndex,seqLength):
                projection.append(sequence[index])
            if projection:
                #print("\nProjection Found as"+str(projection) )
                projectionDB.append(projection)
    return projectionDB

def findItemSupport(item,seqSet):
    support = 0
    for sequence in seqSet:
        for elem in sequence:
            if item in elem:
                support += 1
                break
    return support

def getParam():
    f = open(configPath, 'r')
    minSup = int(f.readline())
    return minSup

def getSeq():
    seqSet = []
    with open(dataPath, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            #print ("\n"+str(row))
            Seq = []
            for elem in row:
                seqElem = list(elem)
                seqElem.sort()
                Seq.append(seqElem)
            seqSet.append(Seq)
    return seqSet

main()