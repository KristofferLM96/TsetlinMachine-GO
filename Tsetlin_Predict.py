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
        lineds = [str(x) for x in line.strip().split(',')]
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

def predictSum(boards):
    newArray = np.array(boards)
    print(m.predict2(newArray))

def predictBoards(start,stop, boards,result):
    newArray = np.array(boards[start:stop])
    print(result[start:stop])
    print(m.predict2(newArray))
    for i in range(stop):
        print(Y_train[i])
        print("Board number: "+str(i))
        allpossible, allnumb = findEmpty(X_train[i], "b")
        predictSum(allpossible)
print("----------------------------------------------------------------")


predictBoards(0,100,X_train, Y_train)

