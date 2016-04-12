from __future__ import print_function
import itertools
import csv
import copy
import time

dataPath = '/home/aeon/Proj2/GSP/DATASET6.csv'
configPath = '/home/aeon/Proj2/GSP/Parameters6.config'

def main():
    seqSet = getSeq()
    minSup = getParam()
    print ("\n Sequences : "+ str(seqSet)+"\n MinSup : "+str(minSup))
    start = time.clock()
    freqSequences = GSP(seqSet,minSup)
    end = time.clock()
    print ("\nFrequent Sequences\n------------------")
    freqCount = 0
    for seqset in freqSequences:
        freqCount +=len(seqset)
        print ("\n"+str(freqSequences.index(seqset) + 1)+" Frequent Sequences\n--------------------")
        for seq in seqset:
            print ("\n", end="")
            count = len(seq)
            for elem in seq:
                for item in elem:
                    print (item, end = "")
                count -= 1
                if count > 0:
                    print (",", end = "")
    print ("\nNumber of Sequences found : "+str(freqCount))
    print ("\nTime Taken : "+str(end - start))

def GSP(seqSet,minSup):
    freqSequences = []
    curSeq = []
    curFreqSeq = []
    k = 1
    for sequence in seqSet:
        for element in sequence:
            for item in element:
                if [item ] not in curSeq :
                    curSeq.append([item])
    #print ("\n1 Length Sequence : " + str(curSeq))
    for sequence in curSeq:
        #print ("\n Support for "+str(sequence)+":"+str(findSupport(sequence,seqSet)))
        if findSupport(sequence,seqSet) >= minSup:
            curFreqSeq.append(sequence)
    #print ("\n1 Frequent Sequence : " + str(curFreqSeq))  
    freqSequences.append(curFreqSeq)
    k = 2
    curSeq = []
    for permSet in list(itertools.permutations(curFreqSeq,2)):
        curSeq.append(list(permSet))
    #Adding Diagonal Permutations
    for seq in curFreqSeq:
        curSeq.append([seq,seq])
    #print ("\n Permutations : "+str(curSeq))
    #Adding 2 length Candidates
    curList = []
    for seq in curFreqSeq:
        curList.append(seq[0])
    #print ("\nList : "+str(curList))
    for combSet in list(itertools.combinations(curList,2)):
        curSeq.append([list(combSet)])
    #print ("\n 2 length Candidates : "+str(len(curSeq)))
    curFreqSeq = []
    for sequence in curSeq:
        #print ("\n Support for "+str(sequence)+":"+str(findSupport(sequence,seqSet)))
        if findSupport(sequence,seqSet) >= minSup:
            curFreqSeq.append(sequence)
    #print ("\n2 Frequent Sequence : " + str(curFreqSeq))
    freqSequences.append(curFreqSeq)
    #Generating rest of the Frequent Sequences
    while curFreqSeq:
        curSeq = []
        curFreqSeq2 = copy.deepcopy(curFreqSeq)
        for sequence in curFreqSeq:
            #print ("\nChecking For "+str(sequence)) 
            for item1 in sequence[0]:
                checkSeq = copy.deepcopy(sequence)
                inseq = checkSeq[0]
                in1 = inseq.index(item1)
                del checkSeq[0][in1]
                #removing possible empty element
                if [] in checkSeq:
                    checkSeq.remove([])
                #print ("\nCheckSeq Value : "+str(checkSeq))
                #print ("\nSequence Value :"+str(sequence))
                for seq in curFreqSeq2:
                    if cmp(sequence,seq) == 0:
                        continue
                    #print ("\nMatching with "+str(seq))
                    for item2 in seq[len(seq) - 1]:
                        foundSeq = copy.deepcopy(seq)
                        last = copy.deepcopy(foundSeq[len(foundSeq) - 1])
                        foundSeq.remove(last)
                        last.remove(item2)
                        foundSeq.append(last)
                        #print("\nAfter Deletion:"+str(foundSeq))
                        if [] in foundSeq:
                            foundSeq.remove([])
                        #print ("\nFoundSeq : "+str(foundSeq))
                        if cmp(checkSeq,foundSeq) == 0:
                            #print ("\nBoth Matched")
                            addItem = copy.deepcopy(sequence)
                            if len(seq[len(seq) - 1]) > 1:
                                addItem[len(addItem) - 1].append(item2)
                            else:
                                addItem.append([item2])
                            if len(curSeq) == 0:
                                #print ("\n Adding Item :"+str(addItem))
                                curSeq.append(addItem)
                            else:
                                #print ("\nCurSeq Length Not Equal To Zero")
                                copyList = copy.deepcopy(curSeq)
                                #print ("\n Current CurSeq : "+str(copyList))
                                exists = False
                                for sequen in copyList:
                                    if sequenCompare(addItem,sequen):    
                                        exists = True
                                        break
                                if not exists:
                                    #print ("\n Adding Item :"+str(addItem))
                                    curSeq.append(addItem)
        #print("\nCandidates : "+str(len(curSeq)))
        #Pruning Candidates
        pruneList = []
        for sequence in curSeq:
            for elem in sequence:
                for item in elem:
                    copyElem = copy.deepcopy(elem)
                    copyElem.remove(item)
                    copySeq = copy.deepcopy(sequence)
                    if copyElem:
                        index = copySeq.index(elem)
                        copySeq[index] = copyElem
                    else:
                        copySeq.remove(elem)      
                    if not copySeq in curFreqSeq:
                        pruneList.append(sequence)
                        break
        prunedCandidates = []
        for sequence in curSeq:
            if sequence not in pruneList:
                prunedCandidates.append(sequence)
        #print ("\nPruned Candidates : " + str(prunedCandidates))
        curFreqSeq = []
        k +=1
        for sequence in prunedCandidates:
            if findSupport(sequence,seqSet) >= minSup:
                curFreqSeq.append(sequence)
        #print (str(k)+" Frequent Sequence : "+str(curFreqSeq))
        if curFreqSeq:
            freqSequences.append(curFreqSeq)
    return freqSequences         

def sequenCompare(sequence1,sequence2):
    if len(sequence1) != len(sequence2):
        return False
    index = 0
    for elem in sequence1:
        if set(elem) == set(sequence2[index]):
            index += 1
        else:
            return False
    return True    

def findSupport(sequence,seqSet):
    support = 0
    #print ("\n Finding Support For : "+str(sequence))
    for seq in seqSet:
        #print ("\nComparing With Sequence : "+str(seq)+"With Length : "+str(len(seq)))
        elemIndex = 0
        elemNotFound = False
        count = len(sequence)
        #print("\nCount value set to : "+str(count))
        for element in sequence:
            #print ("\n Checking For Element : "+str(element))
            while elemIndex < len(seq) :
                #print("\nIndex Value : "+str(elemIndex)+"\nComparing With Element "+str(seq[elemIndex]))
                elemEqual = compareElems(element,seq[elemIndex])
                if elemEqual :
                    #print ("\n Element "+str(element)+" Found,Incrementing Index")
                    elemIndex += 1
                    count -= 1
                    #print("\nDecrementing Count\nNew Count : "+str(count))
                    if elemIndex == len(seq) and count != 0:
                        #print("\nElement"+str(element)+" Not Found")
                        elemNotFound = True
                    break
                else:
                    if elemIndex == len(seq) - 1 :
                        #print ("\nElement"+str(element)+" Not Found")
                        elemNotFound = True
                        break
                    else:
                        #print ("\nComparison Failed, Incrementing Index")
                        elemIndex += 1
            if elemNotFound :
                #print ("\nElement "+str(element)+" Not Found In Sequence "+str(seq))
                break
        if not elemNotFound:
            #print ("\nSequence "+str(sequence)+" Found in Sequence "+str(seq))
            support += 1
    #print ("\nSequence Found To Be"+str(sequence)+" With Support value : "+str(support))
    return support

def compareElems(element1,element2):
    count = len(element1)
    for item in element1:
        if item in element2:
            count -= 1
    if count == 0:
        return True
    return False

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
                Seq.append(seqElem)
            seqSet.append(Seq)
    return seqSet

main()