import random

itemSet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

DATASET_LIMIT = 100
ELEM_LIMIT = 15
#ITEM_LIMIT = len(itemSet)
ITEM_LIMIT = 8

outPath = 'DATASET6.csv'

def main():
    with open(outPath,'w') as outFile:
        for i in range(0,DATASET_LIMIT):
            elemLimit = random.randrange(1,ELEM_LIMIT+1,1)
            outString = ""
            for j in range(0,elemLimit):
                itemLimit = random.randrange(1,ITEM_LIMIT+1,1)
                outElem = ""
                for k in range(0,itemLimit):
                    while(True):
                        item = random.choice(itemSet)
                        if item not in outElem:
                            outElem = outElem + item
                            break
                outString = outString + outElem
                if j != elemLimit - 1:
                    outString = outString + ","
            if i != DATASET_LIMIT - 1: 
                outString = outString + "\n"
            outFile.write(outString)
        outFile.close()        

main()