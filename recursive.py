from pyTsetlinMachineParallel.tm import MultiClassTsetlinMachine
from pyTsetlinMachineParallel.tm import MultiClassConvolutionalTsetlinMachine2D
import numpy as np
machine = "TM"
name = "Trond"
#name = "Kristoffer"
#dim = "9x9Natsukaze_"
#dim = "90_9x9Aya_"
#loadfile = "0302-1057"
#loadfile = "0304-1027"
dim = "90_100T_9x9Aya_"
#loadfile = "0310-1211"
loadfile = "0310-1342"
inndata = "Draw"
numb = "0"
numbboard = 88
global X_train,Y_train,X_test,Y_test,m, loadedstate
def init(dim, machine, loadfile):
    global X_train, Y_train, X_test, Y_test, m, loadedstate
    inndata = "Draw"
    boost = 1
    with open("Results/" + name + "/" + machine + "/" + machine + dim + loadfile + ".csv", 'r') as file:
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
        clauses = int(loadarray[2][1][:-2])
        Threshold = int(loadarray[3][1][:-2])
        S = int(loadarray[4][1][:-2])
        if machine == "cTM":
            Window_X = int(loadarray[5][1][:-2])
            Window_Y = int(loadarray[6][1][:-2])
            Shape_X = int(loadarray[7][1][:-2])
            Shape_Y = int(loadarray[8][1][:-2])
            Shape_Z = int(loadarray[9][1][:-2])
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
        m = MultiClassConvolutionalTsetlinMachine2D(clauses, Threshold, S, (Window_X, Window_Y),                                                    boost_true_positive_feedback=boost, weighted_clauses=True)
    loadedstate = np.load("Results/" + "Trond" + "/" + machine + "/" + machine + dim + loadfile +"kFold"+numb + ".npy", allow_pickle=True)
    m.fit(X_train, Y_train, epochs=0, incremental=True)
    m.set_state(loadedstate)

def transform(table,size):
    black = table[:int(len(table)/2)]
    white = table[int(len(table)/2):]
    bwtable = []
    for i in range(size*size):
        if table[i] == table[i+size*size]:
            bwtable.append(".")
        elif table[i] == 1:
            bwtable.append("b")
        elif table[i+size*size]:
            bwtable.append("w")
        else:
            print("Something went wrong!")
    return bwtable
def reform(table,size):
    black = []
    white = []
    for i in range(size*size):
        if table[i] == ".":
            black.append(0.)
            white.append(0.)
        elif table[i] == "b" or table[i] == "B":
            black.append(1.)
            white.append(0.)
        elif table[i] == "w" or table[i] == "W":
            white.append(1.)
            black.append(0.)
        else:
            print("Something went wrong!!")
    return black+white
def printableTable(table, size):
    underline =      ["A","B","C","D","E","F","G","H","I              "]
    mellomrom = "  "
    printTable = []
    printTable.append("-------------------------------------------")
    printTable.append("Correct outcome: %i Predicted outcome: %i     " % (Y_train[numbboard], table[4]))
    scoreLine = "%s Move: %s Score: %i            " % (table[3], table[2], table[5][0])
    printTable.append(scoreLine+length(table[5][0]))

    for column in range(size):
        start = str(size-column)+mellomrom
        tableLine = start
        for row in range(size):
            tableLine += table[1][size*column+row] + mellomrom
        tableLine+= mellomrom+mellomrom+mellomrom+mellomrom+mellomrom+mellomrom+mellomrom
        printTable.append(tableLine)
    uLine = "   "
    for i in range(size):
        uLine +=underline[i] + mellomrom
    printTable.append(uLine)
    return printTable
def length(numb): #alters space depending on length of score
    mellomrom = ""
    for i in range(6-int(len(str(numb)))):
        mellomrom += " "
    return mellomrom
def printTable(table,position):
    mellomrom = "                                            "
    line = ""
    for i in range(position):
        line +=mellomrom
    for row in table:
        print(line+row)
counter = 0
def moveTransform(number,size): #change the moves into letter/number variation
    if(number < 0): return "Start     "
    Alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
    a = int(number/size)
    b = number%size
    return alphabet[b]+str(size-a)+"        "
def findEmpty(table, player,size,tm):
    global counter
    alteredTables = []
    for i in range(len(table[1])):
        if table[1][i] == ".":
            tempTable = np.copy(table[0])
            tempTable2 = tableCopy(table[1])
            tempTable2[i] = player
            if player == "B":
                tempTable[i] = 1
            else:
                tempTable[i + 81] = 1
            outcome, score = predictSum(tm,tempTable)
            alteredTables.append([tempTable,tempTable2,moveTransform(i,9),player, outcome[0], score])
    alteredTables = topFive(alteredTables,player)
    for i in range(len(alteredTables)):
        alteredTables[i].append(printableTable(
            [alteredTables[i][0], alteredTables[i][1], alteredTables[i][2], alteredTables[i][3], alteredTables[i][4],
             alteredTables[i][5]], size))
    return alteredTables
def tableCopy(table):
    newTable = []
    for i in range(len(table)):
        newTable.append(table[i])
    return newTable
def recursive(bwtable,player,size,moves,tm):
    if moves == 0: return bwtable
    moves -= 1
    newBoards = findEmpty(bwtable,player,size,tm)
    for i in newBoards:
        if i[3] == "B":
            nplayer = "W"
        else:
            nplayer = "B"
        i.append(recursive(i, nplayer, size, moves,tm))
    bwtable.append(newBoards)
    #bwtable[0] have bitboard
    #bwtable[1] have black/white table
    #bwtable[2] have converted moves,
    #bwtable[3] have player
    #bwtable[4] have outcome
    #bwtable[5] have score make as table? tmscore = index 0 go score =index 1 or vice versa
    #bwtable[6] have printableoutput
    #bwtable[7] have list of top5 children nodes (newBoards)
    return bwtable
def predictSum(tm, boards):
    newArray = np.array([boards])
    result = tm.predict2(newArray)
    outcome = result[0]
    score = result[1]
    return outcome, score
def topFive(boards, player):
    whiteBoard = []
    blackBoard = []
    drawBoard = []
    for board in boards:
        if board[4] == 0:
            whiteBoard.append(board)
        if board[4] == 1:
            blackBoard.append(board)
        if board[4] == 2:
            drawBoard.append(board)
    if player == "W":
        if len(whiteBoard) == 5:
            return whiteBoard
        elif len(whiteBoard) > 5:
            return topFiveCalculate(whiteBoard, 5)
        elif len(whiteBoard) < 5:
            if len(whiteBoard) +len(drawBoard) == 5:
                return whiteBoard + drawBoard
            elif len(whiteBoard) + len(drawBoard) > 5:
                return whiteBoard + topFiveCalculate(drawBoard, 5-len(whiteBoard))
            elif len(whiteBoard) + len(drawBoard) < 5:
                return whiteBoard + drawBoard + bottomFiveCalculate(blackBoard, 5 - len(whiteBoard)-len(drawBoard))
    if player == "B":
        if len(blackBoard) == 5:
            return blackBoard
        elif len(blackBoard) > 5:
            return topFiveCalculate(blackBoard,5)
        elif len(blackBoard) < 5:
            if len(blackBoard) +len(drawBoard) == 5:
                return blackBoard + drawBoard
            elif len(blackBoard) + len(drawBoard) > 5:
                return blackBoard + topFiveCalculate(drawBoard, 5-len(blackBoard))
            elif len(blackBoard) + len(drawBoard) < 5:
                return blackBoard + drawBoard + bottomFiveCalculate(whiteBoard, 5 - len(blackBoard)-len(drawBoard))
def topFiveCalculate(boards, numb):
    list =[]
    for i in range(numb):
        tempScore = 0
        tempID = 0
        for j in range(len(boards)):
            if abs(boards[j][5][0]) > tempScore:
                tempScore = abs(boards[j][5][0])
                tempID = j
        boards, list = sortList(boards, list, tempID)
    return list
def bottomFiveCalculate(boards,numb):
    list = []
    for i in range(numb):
        tempScore = 0
        tempID = 0
        for j in range(len(boards)):
            if abs(boards[j][5][0]) < tempScore:
                tempScore = abs(boards[j][5][0])
                tempID = j
        boards, list = sortList(boards,list,tempID)
    return list
def sortList(boards,list,iD):
    newList = []
    list.append(boards[iD])
    for i in range(len(boards)):
        if i != iD:
            newList.append(boards[i])
    return newList, list

def main():
    moves = 2
    size = 9
    player = "B"
    init(dim,machine,loadfile)
    initBoard = X_train[numbboard]
    newArray = np.array([initBoard])
    result = m.predict2(newArray)
    outcome = result[0]
    score = result[1]
    bwtable = transform(initBoard, size)
    bwTable = [initBoard,bwtable, "Initial   ", player, outcome, score]
    pTable = printableTable(bwTable, size)
    bwTable.append(pTable)
    tree = recursive(bwTable, player, size, moves,m)
    printTree(tree,0)
def printTree(table, pos):
    printTable(table[6], pos)
    for i in range(13):
        print(table[7][0][6][i]+table[7][1][6][i]+table[7][2][6][i]+table[7][3][6][i]+table[7][4][6][i])
    for i in range(len(table[7])):
        if(len(table[7][i])) == 9:
            printTree(table[7][i],i)
main()


