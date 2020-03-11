from pyTsetlinMachineParallel.tm import MultiClassTsetlinMachine
from pyTsetlinMachineParallel.tm import MultiClassConvolutionalTsetlinMachine2D
import numpy as np
machine = "TM"
#dim = "9x9Natsukaze_"
#dim = "90_9x9Aya_"
dim = "90_100T_9x9Aya_"
#loadfile = "0310-1211"
loadfile = "0310-1342"
#loadfile = "0302-1057"
#loadfile = "0304-1027"

inndata = "Draw"
numb = "0"
boost = 1
numbboard = 4
global X_train,Y_train,X_test,Y_test,m

with open("Results/" + "Trond" + "/" + machine + "/" + machine + dim + loadfile + ".csv", 'r') as file:
    loadarray = []
    for line in file.readlines():
        # print(line)
        lineds = [str(x) for x in line.strip().split(',')]
        # print (lineds)
        # linesd = str(lineds[0])
        if lineds[-1] == "":
            loadarray.append(lineds[:-1])
        else:
            loadarray.append(lineds)
    if loadarray[0][0][10] == "T":
        machine = "TM"
    else:
        machine = "cTM"
    kFoldstart = 0
    clauses = int(loadarray[2][1][:-2])
    Threshold = int(loadarray[3][1][:-2])
    S = int(loadarray[4][1][:-2])
    if machine == "TM":
        kFoldstart = 5
    if machine == "cTM":
        Window_X = int(loadarray[5][1][:-2])
        Window_Y = int(loadarray[6][1][:-2])
        Shape_X = int(loadarray[7][1][:-2])
        Shape_Y = int(loadarray[8][1][:-2])
        Shape_Z = int(loadarray[9][1][:-2])
        kFoldstart = 10
train_data = np.loadtxt("Data/" + dim + inndata + numb + "train", delimiter=",")
test_data = np.loadtxt("Data/" + dim + inndata + numb + "test", delimiter=",")
if machine == "TM":
    X_train = train_data[:, 0:-1]
    Y_train = train_data[:, -1]
    X_test = test_data[:, 0:-1]
    Y_test = test_data[:, -1]
    m = MultiClassTsetlinMachine(clauses, Threshold, S, boost_true_positive_feedback=boost, weighted_clauses=True)
if machine == "cTM":
    X_train = train_data[:, 0:-1].reshape(train_data.shape[0], Shape_X, Shape_Y, Shape_Z)
    Y_train = train_data[:, -1]
    X_test = test_data[:, 0:-1].reshape(test_data.shape[0], Shape_X, Shape_Y, Shape_Z)
    Y_test = test_data[:, -1]
    m = MultiClassConvolutionalTsetlinMachine2D(clauses, Threshold, S, (Window_X, Window_Y),
                                                boost_true_positive_feedback=boost, weighted_clauses=True)

loadedstate = np.load("Results/" + "Trond" + "/" + machine + "/" + machine + dim + loadfile +"kFold"+numb + ".npy", allow_pickle=True)
m.fit(X_train, Y_train, epochs=0, incremental=True)
m.set_state(loadedstate)

def convertBoard(board):
    black =board[:int(len(board)/2)]
    white = board[int(len(board) / 2):]
    newBoard = []
    for i in range(len(black)):
        if black[i] == 1:
            newBoard.append("b")
        elif white[i] == 1:
            newBoard.append("w")
        else:
            newBoard.append(".")
    return newBoard
def convertBoard2(board,numb):
    black =board[:int(len(board)/2)]
    white = board[int(len(board) / 2):]
    newBoard = []
    for i in range(len(black)):
        if i == numb:
            newBoard.append("B")
        elif black[i] == 1:
            newBoard.append("b")
        elif white[i] == 1:
            newBoard.append("w")
        else:
            newBoard.append(".")
    return newBoard
def findEmpty(board, side):
    boards = []
    number = []
    for i in range(int(len(board)/2)):
        if board[i] == 0 and board[i+81] == 0:
            newBoard = np.copy(board)
            if side == "b":
                newBoard[i] = 1
                number.append(i)
            else:
                newBoard[i+81] = 1
                number.append(i+81)
            boards.append(newBoard)

    return boards, number

def printBoard(board, size):
    #print(board)
    counter = 0
    countdown = 0
    newLine = ""+str(9)
    for i in range(len(board)):
        newLine = newLine + " " + board[i]
        counter += 1
        if (counter == size):
            counter = 0
            countdown +=1
            print(newLine)
            newLine = ""+str(9-countdown)
    print("  A B C D E F G H I")
def predictSum(boards,numbs):
    print("boards")
    print(boards)
    newArray = np.array(boards)
    print("newArray")
    print(newArray)
    print(m.predict2(newArray))
    result = m.predict2(newArray)
    outcome = result[0]
    score = result[1]
    for i in range(len(boards)):
        converted = convertBoard2(boards[i], numbs[i])
        print("----------------------------------------------------------------")
        #print("Correct outcome: %.1f" % (Y_train))
        print("Correct outcome: %.1f Predicted outcome: %s " % (Y_train[numbboard], outcome[i]))
        print("Score: %i "%(score[i]))
        printBoard(converted,9)
        print("----------------------------------------------------------------")
def runM():
    numbboard = 4
    convBoard = convertBoard(X_train[numbboard])
    printBoard(convBoard, 9)
    print(Y_train[numbboard])
    newArray = np.array([X_train[numbboard]])
    print("newArray")
    print(newArray)
    print(m.predict2(newArray))
    result = m.predict2(newArray)
    outcome = result[0]
    score = result[1]
    print(outcome)
    print(score)
    print("----------")
    allpossible,allnumb = findEmpty(X_train[numbboard], "b")
    #for i in range(len(allpossible)):
    #    convBoard = convertBoard(allpossible[i])
    #    printBoard(convBoard, 9)
    predictSum(allpossible,allnumb)
    print("----------------------------------------------------------------")
    print("----------------------------------------------------------------")
    print("----------------------------------------------------------------")
    print("----------------------------------------------------------------")
    numbboard = 9
    convBoard = convertBoard(X_train[numbboard])
    printBoard(convBoard, 9)
    print(Y_train[numbboard])
    print("----------")
    allpossible,allnumb = findEmpty(X_train[numbboard], "b")
    predictSum(allpossible,allnumb)
    convBoard = convertBoard(X_train[numbboard])
    printBoard(convBoard, 9)
    print(Y_train[numbboard])
    print("----------")
    allpossible,allnumb = findEmpty(X_train[numbboard], "b")
    print("----------------------------------------------------------------")
    print("----------------------------------------------------------------")
    print("----------------------------------------------------------------")
    print("----------------------------------------------------------------")
    numbboard = 10
    convBoard = convertBoard(X_train[numbboard])
    printBoard(convBoard, 9)
    print(Y_train[numbboard])
    print("----------")
    allpossible,allnumb = findEmpty(X_train[numbboard], "b")
    predictSum(allpossible,allnumb)
    print("----------------------------------------------------------------")
    print("----------------------------------------------------------------")
    print("----------------------------------------------------------------")
    print("----------------------------------------------------------------")
    numbboard = 19
    newArray = X_train

def predictBoards(start,stop, boards,result):
    newArray = np.array(boards[start:stop])
    print(result[start:stop])
    print(m.predict2(newArray))
    results = m.predict2(newArray)
    outcome = results[0]
    score = results[1]
    for i in range(len(boards)-1):
        converted = convertBoard(boards[i])
        print("----------------------------------------------------------------")
        #print("Correct outcome: %.1f" % (Y_train))
        print("Correct outcome: %.1f Predicted outcome: %s " % (result[i], outcome[i]))
        print("Score: %i "%(score[i]))
        printBoard(converted,9)
        print("----------------------------------------------------------------")
print("----------------------------------------------------------------")
print("----------------------------------------------------------------")
print("----------------------------------------------------------------")
print("----------------------------------------------------------------")

predictBoards(0,100,X_train, Y_train)

#ttrain = m.transform(X_train[4],inverted = False)
#print(Y_train[4])
#print(ttrain)
#print(loadedstate)
#class0 = loadedstate[0][0]
#class1 = loadedstate[1][0]
#class2 = loadedstate[2][0]
#zsum = 0
#zsumn = 0
#osum = 0
#osumn = 0
#tsum = 0
#tsumn = 0
#print(len(class0))
#print(len(class1))
#print(len(class2))
#print(len(ttrain))
#for i in range(len(ttrain[0])):
#    if i%2==0:
#        zsum += class0[i] *ttrain[i]
#        osum += class1[i] * ttrain[i]
#        tsum += class2[i] * ttrain[i]
#    else:
#        zsumn += class0[i] *ttrain[i]
#        osumn += class1[i] * ttrain[i]
#        tsumn += class2[i] * ttrain[i]
#print(zsum + "  " +zsumn)
#print(osum + "  " +osumn)
#print(tsum + "  " +tsumn)

