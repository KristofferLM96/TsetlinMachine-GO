import csv
from numpy.random import shuffle

win = open("Data/Results-Split/9x9Natsukaze_win.txt", 'r')
loss = open("Data/Results-Split/9x9Natsukaze_loss.txt", 'r')
draw = open("Data/Results-Split/9x9Natsukaze_draw.txt", 'r')
win_line = win.readlines()
loss_line = loss.readlines()
draw_line = draw.readlines()
shuffle(win_line)
shuffle(loss_line)
shuffle(draw_line)
print("Amount of wins: ", len(win_line))
print("Amount of loss: ", len(loss_line))
print("Amount of draw: ", len(draw_line))
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
collection = [table0, table1, table2, table3, table4, table5, table6, table7, table8, table9]
collection2 = [table10, table11, table12, table13, table14, table15, table16, table17, table18, table19]


def split():
    i = 0
    for row in win_line:
        collection[i].append(row)
        collection2[i].append(row)
        i += 1
        if i == 10:
            i = 0
    i = 0
    for row in loss_line:
        collection[i].append(row)
        collection2[i].append(row)
        i += 1
        if i == 10:
            i = 0
    i = 0
    for row in draw_line:
        collection2[i].append(row)
        i += 1
        if i == 10:
            i = 0


def getList(_input):
    list = []
    for i in _input:
        list.append(i)
    return list


def makeSet(_input, i):
    j = 0
    test = []
    train = []
    while j < 10:
        if i == j:
            test = getList(_input[j])
        else:
            train = train + getList(_input[j])
        j += 1
    return train, test


def shuffleWrite(train, test, _input, i):
    temp1, temp2 = makeSet(_input, i)
    shuffle(temp1)
    shuffle(temp2)
    for j in temp1:
        train.write(j)
    for k in temp2:
        test.write(k)


split()
i = 0
while i < 10:
    train_numb = str(i)+"train"
    test_numb = str(i)+"test"
    no_draw_train = open("Data/K-Fold/No-Draw/9x9Natsukaze_NoDraw"+train_numb, 'w')
    no_draw_test = open("Data/K-Fold/No-Draw/9x9Natsukaze_NoDraw"+test_numb, 'w')
    draw_train = open("Data/K-Fold/Draw/9x9Natsukaze_Draw"+train_numb, 'w')
    draw_test = open("Data/K-Fold/Draw/9x9Natsukaze_Draw"+test_numb, 'w')
    shuffleWrite(no_draw_train, no_draw_test, collection, i)
    shuffleWrite(draw_train, draw_test, collection2, i)
    i += 1
