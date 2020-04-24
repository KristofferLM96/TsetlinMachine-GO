from pyTsetlinMachineParallel.tm import MultiClassTsetlinMachine
from pyTsetlinMachineParallel.tm import MultiClassConvolutionalTsetlinMachine2D
import numpy as np
import time as stime
import tm_predict as predict
import go_board_play as go_board


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
###################
#numbboard = 654
#numbboard = 566
#numbboard = 868
numbboard = 91
depth = 3   #number of moves
tree_width = 4
#save_file = "91-5-4"
save_file = "TM_play"
##################
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

def printableTable(table, size,turns):
    underline =      ["A","B","C","D","E","F","G","H","I              "]
    mellomrom = "  "
    printTable = []
    printTable.append("-------------------------------------------")
    #print(table[4][-1])
    #print(table[4][-1][0])
    printTable.append("Turn: %i Predicted outcome: %i     " % (70-turns, table[4][-1][0]))
    for i in range(len(table[3])):
        scoreLine= "%s Move: %s Score: %i (%s)(%s)   " % (table[3][i], table[2][i], table[5][i],table[4][i][0],table[4][i][1])
        printTable.append(scoreLine+length(table[5][i],6)+length(table[4][i][1],3))

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
def length(numb,length): #alters space depending on length of score
    mellomrom = ""
    for i in range(length-int(len(str(numb)))):
        mellomrom += " "
    return mellomrom
def printTable(table,position):
    mellomrom = "                                            "
    line = ""
    for i in range(position):
        line +=mellomrom
    for row in table:
        print(line+row)
        results.write(line+row + "\n")
counter = 0
def moveTransform(number,size): #change the moves into letter/number variation
    if(number < 0): return "Start     "
    Alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
    a = int(number/size)
    b = number%size
    return alphabet[b]+str(size-a)+"        "
def moveReform(text,size): #change the moves into letter/number variation
    Alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
    letter= text[0]
    number = int(text[1])
    for i in range(len(alphabet)):
        if letter == alphabet[i]:
            letter = i
    return size*(size-number)+letter
def findEmpty(table, player,size,width, initResult):
    global b_last_play,w_last_play
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
            #if player == "B" and i != b_last_play or player == "W" and i*81 != w_last_play:
            outcome, score, go_outcome, lossresult, winresult, drawresult, retTable, retBw = predict.predictSum(tempTable2, initResult, player)
            newM = tableCopy(table[2])
            newM.append(moveTransform(i,9))
            newP = tableCopy(table[3])
            newO = tableCopy(table[4])
            newS = tableCopy(table[5])
            newP.append(player)
            newO.append([outcome,go_outcome])
            newS.append(score)
            alteredTables.append([retTable,retBw,newM,newP, newO, newS])
    #print(alteredTables)
    alteredTables = topFive(alteredTables,player, width)
    for i in range(len(alteredTables)):
        alteredTables[i].append(printableTable(
            [alteredTables[i][0], alteredTables[i][1], alteredTables[i][2], alteredTables[i][3], alteredTables[i][4],
             alteredTables[i][5]], size,70))
    return alteredTables
def tableCopy(table):
    newTable = []
    for i in range(len(table)):
        newTable.append(table[i])
    return newTable
end_table = []
def recursive(bwtable,player,size,moves,width, initResult):
    if moves == 0: end_table.append(bwtable)
    if moves == 0: return bwtable
    moves -= 1
    newBoards = findEmpty(bwtable,player,size,width, initResult)
    for i in newBoards:
        if i[3][-1] == "B":
            nplayer = "W"
        else:
            nplayer = "B"
        i.append(recursive(i, nplayer, size, moves,width, initResult))
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

def topFive(boards, player, width):
    number = width #how wide is the search
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
    #whiteBoard = np.random.shuffle(whiteBoard)
    #blackBoard = np.random.shuffle(blackBoard)
    #drawBoard = np.random.shuffle(drawBoard)
    if player == "W":
        if len(whiteBoard) >= number:
            return topFiveCalculate(whiteBoard, number)
        elif len(whiteBoard) < number:
            if len(whiteBoard) +len(drawBoard) == number:
                return topFiveCalculate(whiteBoard,len(whiteBoard)) + topFiveCalculate(drawBoard,len(drawBoard))
            elif len(whiteBoard) + len(drawBoard) > number:
                return topFiveCalculate(whiteBoard,len(whiteBoard))  + topFiveCalculate(drawBoard, number-len(whiteBoard))
            elif len(whiteBoard) + len(drawBoard) < number:
                return topFiveCalculate(whiteBoard,len(whiteBoard)) + topFiveCalculate(drawBoard,len(drawBoard)) + bottomFiveCalculate(blackBoard, number - len(whiteBoard)-len(drawBoard))
    if player == "B":
        if len(blackBoard) >= number:
            return topFiveCalculate(blackBoard,number)
        elif len(blackBoard) < number:
            if len(blackBoard) +len(drawBoard) == number:
                return topFiveCalculate(blackBoard,len(blackBoard)) + topFiveCalculate(drawBoard,len(drawBoard))
            elif len(blackBoard) + len(drawBoard) > number:
                return topFiveCalculate(blackBoard,len(blackBoard))+ topFiveCalculate(drawBoard, number-len(blackBoard))
            elif len(blackBoard) + len(drawBoard) < number:
                return topFiveCalculate(blackBoard,len(blackBoard)) + topFiveCalculate(drawBoard,len(drawBoard)) + bottomFiveCalculate(whiteBoard, number - len(blackBoard)-len(drawBoard))
def topFive5(boards, player,number):
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
        if len(whiteBoard) >= number:
            return topFiveCalculate(whiteBoard, number)
        elif len(whiteBoard) == 0:
            return bottomFiveCalculate(blackBoard, number)
        elif len(whiteBoard) < number:
            if len(whiteBoard) +len(drawBoard) == number:
                return topFiveCalculate(whiteBoard,len(whiteBoard)) + topFiveCalculate(drawBoard,len(drawBoard))
            elif len(whiteBoard) + len(drawBoard) > number:
                return topFiveCalculate(whiteBoard,len(whiteBoard))  + topFiveCalculate(drawBoard, number-len(whiteBoard))
            elif len(whiteBoard) + len(drawBoard) < number:
                return topFiveCalculate(whiteBoard,len(whiteBoard)) + topFiveCalculate(drawBoard,len(drawBoard)) + bottomFiveCalculate(blackBoard, number - len(whiteBoard)-len(drawBoard))
    if player == "B":
        if len(blackBoard) >= number:
            return topFiveCalculate(blackBoard,number)
        elif len(blackBoard) == 0:
            return bottomFiveCalculate(whiteBoard, number)
        elif len(blackBoard) < number:
            if len(blackBoard) +len(drawBoard) == number:
                return topFiveCalculate(blackBoard,len(blackBoard)) + topFiveCalculate(drawBoard,len(drawBoard))
            elif len(blackBoard) + len(drawBoard) > number:
                return topFiveCalculate(blackBoard,len(blackBoard))+ topFiveCalculate(drawBoard, number-len(blackBoard))
            elif len(blackBoard) + len(drawBoard) < number:
                return topFiveCalculate(blackBoard,len(blackBoard)) + topFiveCalculate(drawBoard,len(drawBoard)) + bottomFiveCalculate(whiteBoard, number - len(blackBoard)-len(drawBoard))
def topFiveCalculate(boards, numb):
    listallscore = []
    list =[]
    for i in range(numb):
        tempScore = -100000
        tempID = 0
        for j in range(len(boards)):
            listallscore.append(boards[j][5][-1])
            #if abs(boards[j][5][0]) > tempScore:
            if boards[j][5][-1] > tempScore:
                #tempScore = abs(boards[j][5][0])
                tempScore = boards[j][5][-1]
                tempID = j
            if boards[j][5][-1] == tempScore:
                np.random.seed()
                X1 = np.random.randint(low=0, high=10, size=(1))
                if X1[0] > 4:
                    tempScore = boards[j][5][-1]
                    tempID = j
        boards, list = sortList(boards, list, tempID)
    return list
def bottomFiveCalculate(boards,numb):
    listallscore = []
    list = []
    for i in range(numb):
        tempScore = 100000
        tempID = 0
        for j in range(len(boards)):
            listallscore.append(boards[j][5][-1])
            #if abs(boards[j][5][0]) < tempScore:
                #tempScore = abs(boards[j][5][0])
            if boards[j][5][-1] < tempScore:
                tempScore = boards[j][5][-1]
                tempID = j
            if boards[j][5][-1] == tempScore:
                np.random.seed()
                X1 = np.random.randint(low=0, high=10, size=(1))
                if X1[0] > 4:
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

def main(moves, width,X2):
    #moves = 5
    #width= 2
    size = 9
    player = "B"
    timestamp = stime.strftime("%H:%M:%S")
    init(dim,machine,loadfile)
    predict.init(weights, clauses,m,m)
    timestamp2 = stime.strftime("%H:%M:%S")
    initBoard = X2
    initResult = Y_train[numbboard]
    bwtable = transform(initBoard, size)
    outcome, score, percentage, losstot,wintot,drawtot, newbit,newbw = predict.predictSum(bwtable, initResult, player)
    bwTable = [initBoard,bwtable, ["Initial   "], [player], [[outcome,percentage]], [score]]
    pTable = printableTable(bwTable, size,0)
    bwTable.append(pTable)
    tree = recursive(bwTable, player, size, moves,width, initResult)
    timestamp3 = stime.strftime("%H:%M:%S")
    #printTree(tree,0,width)
    print("Start Time        : %s " % (timestamp))
    print("Init finished Time: %s " % (timestamp2))
    print("Predict done Time : %s " % (timestamp3))
    ran =5
    if width == 1:
        ran = 1
    #print(len(end_table))
    printTop(topFive(end_table,"B",ran),ran)
    #printTop(bottomFiveCalculate(end_table,ran),ran)
    print(predict.getTime())
    autoPlay(tree,70,moves, width)
def autoPlay(tree,turns,moves, width):
    if turns == 0: return "Finished"
    playTmGo(tree,turns,moves, width)
def playTmGo(tree,turns,moves, width):
    global end_table, b_last_play,w_last_play
    seconds = int(round(stime.time()))
    np.random.seed()
    X1 = np.random.randint(low=0, high=5, size=(1))
    x_random = X1[0]
    initResult = 2.0
    initBoard =tree[0]
    move = moveReform(end_table[x_random][2][1], 9)
    if end_table[x_random][3][1] == "B":
        initBoard[move] = 1
    else:
        initBoard[move+81] =1
    bwtable = transform(initBoard, 9)
    score, bWtable = go_board.go_calc(bwtable)
    if end_table[x_random][3][1] == "B":
        nplayer = "W"
        b_last_play = move
    else:
        nplayer = "B"
        w_last_play = move+81

    outcome, score, percentage, losstot, wintot, drawtot, newbit, newbw = predict.predictSum(bWtable, initResult, nplayer)
    bwTable = [initBoard, bwtable, [end_table[x_random][2][1]], [end_table[x_random][3][1]], [[outcome, percentage]], [score]]
    bwTable2 = [initBoard, bWtable, [end_table[x_random][2][1]], [end_table[x_random][3][1]], [[outcome, percentage]], [score]]
    pTable = printableTable(bwTable2, 9,turns)
    bwTable.append(pTable)
    printTable(pTable, 1)
    end_table = []
    if nplayer == "B":
        tree = recursive(bwTable, nplayer, 9, moves, width, initResult)
    if nplayer == "W":
        tree = recursive(bwTable, nplayer, 9, moves, 2, initResult)
    turns -=1
    seconds2 = int(round(stime.time()))
    print("Time: %s"%(seconds2-seconds))
    autoPlay(tree, turns,moves, width)


def printTree(table, pos,width):
    printTable(table[6], pos)
    for i in range(len(table[7][0][6])):
        #print(table[7][0][6][i]+table[7][1][6][i]+table[7][2][6][i]+table[7][3][6][i]+table[7][4][6][i]) #if number = 5
        tempTxt = ""
        for j in range(width):
            tempTxt+= table[7][j][6][i]
        print(tempTxt)
        results.write(tempTxt+"\n")
    for i in range(len(table[7])):
        if(len(table[7][i])) == 9:
            printTree(table[7][i],i, width)
def printTop(table, width):
    for i in range(len(table[0][6])):
        tempTxt = ""
        #print(table[0][6][i] + table[1][6][i] + table[2][6][i] + table[3][6][i] + table[4][6][i])
        for j in range(width):
            tempTxt += table[j][6][i]
        print(tempTxt)
        results.write(tempTxt + "\n")

for i in range(10):
    results = open("Results/" + name + "/" + machine + "/" + machine + dim + loadfile + save_file+str(i)+".txt", 'w')
    X2 = []
    for i in range(81):
        X2.append(0)
        X2.append(0)
    b_last_play = 300
    w_last_play = 300
    main(depth, tree_width,X2)
    results.close()