import csv
from numpy.random import shuffle
gowin = open("GoWin9x9.txt",'r')
goloss = open("GoLoss9x9.txt",'r')
godraw = open("GoDraw9x9.txt",'r')
wreader = gowin.readlines()
lreader = goloss.readlines()
dreader = godraw.readlines()
shuffle(wreader)
shuffle(lreader)
shuffle(dreader)
print(len(wreader))
print(len(lreader))
print(len(dreader))
table1 = []
table2 = []
table3 = []
table4 = []
table5 = []
table6 = []
table7 = []
table8 = []
table9 = []
table0 = []
table11 = []
table12 = []
table13 = []
table14 = []
table15 = []
table16 = []
table17 = []
table18 = []
table19 = []
table10 = []
collection = [table0,table1,table2,table3,table4,table5,table6,table7,table8,table9]
collection2 = [table10,table11,table12,table13,table14,table15,table16,table17,table18,table19]

def split():
    i=0
    print(len(wreader))
    print(len(lreader))
    print(len(dreader))
    for row in wreader:
        collection[i].append(row)
        collection2[i].append(row)
        i+=1
        if (i == 10):
            i = 0
    i=0
    for row in lreader:
        collection[i].append(row)
        collection2[i].append(row)
        i += 1
        if (i == 10):
            i = 0
    i=0
    for row in dreader:
        collection2[i].append(row)
        i += 1
        if (i == 10):
            i = 0
    #print(collection)
    #print(collection2)

def getList(input):
    #print(len(input))
    list = []
    for i in input:
        list.append(i)
    #print(len(list))
    #print(input)
    #print(list)
    return list


def makeSet(input, i):
    j = 0
    test = []
    train = []
    while j < 10:
        if(i == j):
            test= getList(input[j])
            #print(""+str(i) + " if " + str(j))
            #print(input[i])
        else:
            train = train + getList(input[j])
            #print(""+str(i) + " else " + str(j))
            #print(input[i])
        j+=1
    return train, test
def shuffleWrite(train, test,input, i):
    temp1, temp2 = makeSet(input,i)
    #print(len(temp1))
    #print(len(temp2))
    shuffle(temp1)
    shuffle(temp2)
    for j in temp1:
        train.write(j)
    for k in temp2:
        test.write(k)

split()
i =0
while i < 10:
    trainnumb = str(i)+"train"
    testnumb = str(i)+"test"
    nodraw = open("./dataset/9x9nodraw"+trainnumb, 'w')
    nodrawtest = open("./dataset/9x9nodraw"+testnumb, 'w')
    draw = open("./dataset/9x9draw"+trainnumb, 'w')
    drawtest = open("./dataset/9x9draw"+testnumb, 'w')
    shuffleWrite(nodraw,nodrawtest, collection,i)
    shuffleWrite(draw, drawtest, collection2, i)
    i+=1