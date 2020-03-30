from pyTsetlinMachineParallel.tm import MultiClassTsetlinMachine
from pyTsetlinMachineParallel.tm import MultiClassConvolutionalTsetlinMachine2D
import gomill.boards
import gomill.ascii_boards
import numpy as np
import time as stime


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
weights = []
clauses= 0
global X_train,Y_train,X_test,Y_test,m, loadedstate
def init(dim, machine, loadfile):
    global X_train, Y_train, X_test, Y_test, m, loadedstate, weights, clauses
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
    weights = m.get_state()

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
    #print(table[4][-1])
    #print(table[4][-1][0])
    printTable.append("Correct outcome: %i Predicted outcome: %i     " % (Y_train[numbboard], table[4][-1][0]))
    for i in range(len(table[3])):
        scoreLine= "%s Move: %s Score: %i   (%s)      " % (table[3][i], table[2][i], table[5][i],table[4][i][0])
        printTable.append(scoreLine+length(table[5][i]))

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
            outcome, score, percentage = predictSum(tm,tempTable)
            newM = tableCopy(table[2])
            newM.append(moveTransform(i,9))
            newP = tableCopy(table[3])
            newO = tableCopy(table[4])
            newS = tableCopy(table[5])
            newP.append(player)
            newO.append([outcome,percentage])
            newS.append(score)
            alteredTables.append([tempTable,tempTable2,newM,newP, newO, newS])
    #print(alteredTables)
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
end_table = []
def recursive(bwtable,player,size,moves,tm):
    if moves == 0: end_table.append(bwtable)
    if moves == 0: return bwtable
    moves -= 1
    newBoards = findEmpty(bwtable,player,size,tm)
    for i in newBoards:
        if i[3][-1] == "B":
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
    result2 = tm.transform(newArray,inverted = False)
    #print(result2[0][0])
    loss = weights[0][0]
    win = weights[1][0]
    draw = weights[2][0]
    outcome = -1
    score = -1
    percentage = 0
    #print("Predicted Result: ",result[0], " ", result[1])
    lossresult = weightedCalc(result2[0][0:clauses],loss)
    winresult = weightedCalc(result2[0][clauses:clauses*2], win)
    drawresult = weightedCalc(result2[0][clauses*2:clauses*3], draw)
    #print("Pos Prediction for loss: %s Prediction for win: %s Prediction for draw: %s" % (lossresult[0],winresult[0],drawresult[0]))
    #print("Neg Prediction for loss: %s Prediction for win: %s Prediction for draw: %s" % (lossresult[1], winresult[1], drawresult[1]))
    #print("Sum Prediction for loss: %s Prediction for win: %s Prediction for draw: %s" % (lossresult[0] - lossresult[1], winresult[0] - winresult[1], drawresult[0] - drawresult[1]))
    losstot = lossresult[0] - lossresult[1]
    wintot = winresult[0] - winresult[1]
    drawtot = drawresult[0] - drawresult[1]
    if losstot > wintot and losstot > drawtot:
        outcome = 0
        score = losstot
        percentage = losstot + drawtot + wintot *100
        percentage = percentage /losstot
    elif wintot > losstot and wintot > drawtot:
        outcome = 1
        score = wintot
        percentage = losstot + drawtot + wintot * 100
        percentage = percentage /wintot
    else:
        outcome = 2
        score = drawtot
        percentage = losstot + drawtot + wintot * 100
        percentage = percentage /drawtot
    #outcome = result[0]
    #score = result[1]
    return outcome, score, percentage
def weightedCalc(clause, weight):
    negs = 0
    ones = 0
    for i in range(len(clause)):
        if clause[i] == 1:
            if i%2 == 0:
                ones += clause[i]*weight[i]
            else:
                negs += clause[i]*weight[i]
    return ones,negs

def topFive(boards, player):
    whiteBoard = []
    blackBoard = []
    drawBoard = []
    for board in boards:
        if board[4][-1][0] == 0:
            whiteBoard.append(board)
        if board[4][-1][0] == 1:
            blackBoard.append(board)
        if board[4][-1][0] == 2:
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
    listallscore = []
    list =[]
    for i in range(numb):
        tempScore = 0
        tempID = 0
        for j in range(len(boards)):
            listallscore.append(boards[j][5][-1])
            #if abs(boards[j][5][0]) > tempScore:
            if boards[j][5][-1] >= tempScore:
                #tempScore = abs(boards[j][5][0])
                tempScore = boards[j][5][-1]
                tempID = j
        boards, list = sortList(boards, list, tempID)
    return list
def bottomFiveCalculate(boards,numb):
    listallscore = []
    list = []
    for i in range(numb):
        tempScore = 0
        tempID = 0
        for j in range(len(boards)):
            listallscore.append(boards[j][5][-1])
            #if abs(boards[j][5][0]) < tempScore:
                #tempScore = abs(boards[j][5][0])
            if boards[j][5][-1] < tempScore:
                tempScore = boards[j][5][-1]
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
    moves = 5
    size = 9
    player = "B"
    timestamp = stime.strftime("%H:%M:%S")
    init(dim,machine,loadfile)
    timestamp2 = stime.strftime("%H:%M:%S")
    initBoard = X_train[numbboard]
    newArray = np.array([initBoard])
    #result = m.predict2(newArray)
    #outcome = result[0]
    #score = result[1]
    outcome, score, percentage = predictSum(m,newArray)
    bwtable = transform(initBoard, size)
    bwTable = [initBoard,bwtable, ["Initial   "], [player], [[outcome,percentage]], [score]]
    pTable = printableTable(bwTable, size)
    bwTable.append(pTable)
    tree = recursive(bwTable, player, size, moves,m)
    timestamp3 = stime.strftime("%H:%M:%S")
    printTree(tree,0)
    print("Start Time        : %s " % (timestamp))
    print("Init finished Time: %s " % (timestamp2))
    print("Predict done Time : %s " % (timestamp3))
    printTop(topFive(end_table,"B"))
    printTop(bottomFiveCalculate(end_table,5))
def printTree(table, pos):
    printTable(table[6], pos)
    for i in range(len(table[7][0][6])):
        print(table[7][0][6][i]+table[7][1][6][i]+table[7][2][6][i]+table[7][3][6][i]+table[7][4][6][i])
    for i in range(len(table[7])):
        if(len(table[7][i])) == 9:
            printTree(table[7][i],i)
def printTop(table):
    for i in range(len(table[0][6])):
        print(table[0][6][i] + table[1][6][i] + table[2][6][i] + table[3][6][i] + table[4][6][i])
main()


