from pyTsetlinMachineParallel.tm import MultiClassTsetlinMachine
from pyTsetlinMachineParallel.tm import MultiClassConvolutionalTsetlinMachine2D
import gomill.boards
import gomill.ascii_boards
import numpy as np
import time as stime
import operator
moves = 1
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
#numb = "0"
#numbboard = 88
numbboard = 388
weights = []
clauses= 0
global X_train,Y_train,X_test,Y_test,m, loadedstate
def init(dim, machine, loadfile, numb):
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

def moveTransform(number,size): #change the moves into letter/number variation
    if(number < 0): return "Start     "
    Alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
    a = int(number/size)
    b = number%size
    return alphabet[b]+str(size-a)+"        "
def findEmpty(table, player,size,tm):
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
            outcome, score, go_outcome, lossresult, winresult, drawresult = predictSum(tm,tempTable,tempTable2)
            #newM = tableCopy(table[2])
            newM = go_outcome
            #newP = tableCopy(table[3])
            #newO = tableCopy(table[4])
            #newS = tableCopy(table[5])
            newP=player
            newO=outcome
            newS = score
            alteredTables.append([tempTable,tempTable2,newM,newP, newO, newS])
    #print(alteredTables)
    #Y_train[numbboard], table[4][-1][0],table[4][-1][1], table[4][-1][2][0], table[4][-1][2][1], table[4][-1][3][0], table[4][-1][3][0], table[4][-1][4][0], table[4][-1][4][1])
    alteredTables = topFive(alteredTables,player)
    return alteredTables
def tableCopy(table):
    newTable = []
    for i in range(len(table)):
        newTable.append(table[i])
    return newTable
end_table1 = []
end_table2 = []
end_table3 = []
end_table4 = []
end_table5 = []
def recursive(bwtable,player,size,moves,tm):
    if moves == 0: end_table5.append(bwtable)
    if moves == 1: end_table4.append(bwtable)
    if moves == 2: end_table3.append(bwtable)
    if moves == 3: end_table2.append(bwtable)
    if moves == 4: end_table1.append(bwtable)
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
def predictSum(tm, boards,boards2):
    newArray = np.array([boards])
    result2 = tm.transform(newArray,inverted = False)
    #print(result2[0][0])
    loss = weights[0][0]
    win = weights[1][0]
    draw = weights[2][0]
    outcome = -1
    score = -1
    go_correct = go_calc(boards2)
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
    elif wintot > losstot and wintot > drawtot:
        outcome = 1
        score = wintot
    else:
        outcome = 2
        score = drawtot
    #outcome = result[0]
    #score = result[1]
    return outcome, score, go_correct, lossresult, winresult, drawresult
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
    number = 2
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
    #print(whiteBoard)
    whiteBoard = sort_table(whiteBoard,5)
    #print(whiteBoard)
    #print(blackBoard)
    blackBoard = sort_table(blackBoard,5)
    #print("------------------------------------------")
    #print(blackBoard)
    drawBoard = sort_table(drawBoard,5)
    #if player == "W":
    #    if(len(whiteBoard) < 1):
    #        if(len(drawBoard) <1):
    #            return [blackBoard[-1]]
    #        else:
    #            return [drawBoard[0]]
    #    else: return [whiteBoard[0]]
    #if player == "B":
    #    if(len(blackBoard) < 1):
    #        if(len(drawBoard) <1):
    #            return [whiteBoard[-1]]
    #        else:
    #            return [drawBoard[0]]
    #    else: return [blackBoard[0]]
    if player == "W":
        if len(whiteBoard) >= number:
            return whiteBoard[0:number]
        elif len(whiteBoard) < number:
            if len(whiteBoard) + len(drawBoard) >= number:
                return whiteBoard + drawBoard[0:number-len(whiteBoard)]
            elif len(whiteBoard) + len(drawBoard) < number:
                return whiteBoard + drawBoard + blackBoard[len(whiteBoard)+len(drawBoard)-number:]
    if player == "B":
        if len(blackBoard) >= number:
            return blackBoard[0:number]
        elif len(blackBoard) < number:
            if len(blackBoard) + len(drawBoard) >= number:
                return blackBoard + drawBoard[0:number-len(blackBoard)]
            elif len(blackBoard) + len(drawBoard) < number:
                #print(blackBoard + drawBoard + whiteBoard[len(blackBoard)+len(drawBoard)-5:])
                return blackBoard + drawBoard + whiteBoard[len(blackBoard)+len(drawBoard)-number:]
def sort_table(table, col):
    return sorted(table, key=operator.itemgetter(col), reverse=True)
def main(sort):
    global end_table1,end_table2,end_table3,end_table4,end_table5,moves
    moves = 5
    results = open("Results/" + name + "/" + machine + "/" + machine + dim + loadfile + "tree"+sort+".txt", 'a')
    results.close()
    timestamp = stime.strftime("%H:%M:%S")
    print("Start Time        : %s " % (timestamp))
    numb = "0"
    init(dim,machine,loadfile,numb)
    timestamp2 = stime.strftime("%H:%M:%S")
    print("Init finished Time: %s " % (timestamp2))
    invalid_counter = 0
    counter = [0,0,0,0,0]
    wcounter = [0,0,0,0,0]
    lcounter = [0,0,0,0,0]
    dcounter = [0,0,0,0,0]
    counter_r = [0,0,0,0,0]
    wcounter_r = [0,0,0,0,0]
    lcounter_r = [0,0,0,0,0]
    dcounter_r = [0,0,0,0,0]
    print(len(X_test))
    print(len(X_train))
    printnumb = 1
    printnumb2 = 1
    for numbboard in range(10060):
        #numbboard+=40000
        #print(numbboard)
        if (counter[0] == printnumb2 * 1000):
            tempTime = stime.strftime("%H:%M:%S")
            print("Time: %s Done: %s Total: %s" % (tempTime, printnumb2 * 1000, 10000))
            for i in range(5):
                print("Moves: %s Total : %s/%s Loss: %s/%s Win: %s/%s Draw: %s/%s" % (i+1,
                    counter_r[i], counter[i], lcounter_r[i], lcounter[i], wcounter_r[i], wcounter[i], dcounter_r[i],
                    dcounter[i]))
            print("Invalid board: %s" % (invalid_counter))
            printnumb2 += 1
        if(counter[0] == printnumb*5000):
            tempTime = stime.strftime("%H:%M:%S")
            print("Time: %s Done: %s Total: %s"%(tempTime,printnumb*5000,10000))
            results = open("Results/" + name + "/" + machine + "/" + machine + dim + loadfile + "tree" + sort + ".txt",
                           'a')
            results.write("Time: %s Done: %s Total: %s\n"%(tempTime,printnumb*5000,10000))
            for i in range(5):
                print("Moves: %sT otal : %s/%s Loss: %s/%s Win: %s/%s Draw: %s/%s" % (i+1,
                counter_r[i], counter[i], lcounter_r[i], lcounter[i], wcounter_r[i], wcounter[i], dcounter_r[i],
                dcounter[i]))
                results.write("%s Moves: %s Total : %s/%s Loss: %s/%s Win: %s/%s Draw: %s/%s\n" % (
                    sort, i + 1, counter_r[i], counter[i], lcounter_r[i], lcounter[i], wcounter_r[i], wcounter[i],
                    dcounter_r[i],
                    dcounter[i]))
            results.close()
            printnumb+=1
        size = 9
        player = "B"
        for i in range(5):
            counter[i]+=1
        initBoard = X_train[numbboard]
        if sort == "test":
            initBoard = X_test[numbboard]

        if sum(initBoard) < 73:
            initResult = Y_train[numbboard]
            if sort == "test":
                initResult = Y_test[numbboard]
            newArray = np.array([initBoard])
            bwtable = transform(initBoard, size)

            outcome, score, percentage, losstot,wintot,drawtot = predictSum(m,newArray, bwtable)
            bwTable = [initBoard,bwtable, percentage, player, outcome, score]
            tree = recursive(bwTable, player, size, moves,m)
            fivetable1 = topFive(end_table1,"B")
            table1 = fivetable1[0]
            fivetable2 = topFive(end_table2, "B")
            table2 = fivetable2[0]
            fivetable3 = topFive(end_table3, "B")
            table3 = fivetable3[0]
            fivetable4 = topFive(end_table4, "B")
            table4 = fivetable4[0]
            fivetable5 = topFive(end_table5, "B")
            table5 = fivetable5[0]
            if initResult == 0:
                for i in range(5):
                    lcounter[i]+=1
                if table1[2] < 0:
                    lcounter_r[0]+=1
                    counter_r[0] +=1
                if table2[2] < 0:
                    lcounter_r[1]+=1
                    counter_r[1] +=1
                if table3[2] < 0:
                    lcounter_r[2]+=1
                    counter_r[2] +=1
                if table4[2] < 0:
                    lcounter_r[3]+=1
                    counter_r[3] +=1
                if table5[2] < 0:
                    lcounter_r[4]+=1
                    counter_r[4] +=1
            elif initResult == 1:
                for i in range(5):
                    wcounter[i] += 1
                if table1[2] > 0:
                    wcounter_r[0] += 1
                    counter_r[0] +=1
                if table2[2] > 0:
                    wcounter_r[1]+=1
                    counter_r[1] +=1
                if table3[2] > 0:
                    wcounter_r[2]+=1
                    counter_r[2] +=1
                if table4[2] > 0:
                    wcounter_r[3]+=1
                    counter_r[3] +=1
                if table5[2] > 0:
                    wcounter_r[4]+=1
                    counter_r[4] +=1
            else:
                for i in range(5):
                    dcounter[i]+=1
                if table1[2] == 0:
                    dcounter_r[0] += 1
                    counter_r[0] +=1
                if table2[2] == 0:
                    dcounter_r[1] += 1
                    counter_r[1] +=1
                if table3[2] == 0:
                    dcounter_r[2] += 1
                    counter_r[2] +=1
                if table4[2] == 0:
                    dcounter_r[3] += 1
                    counter_r[3] +=1
                if table5[2] == 0:
                    dcounter_r[4] += 1
                    counter_r[4] +=1
            end_table1 = []
            end_table2 = []
            end_table3 = []
            end_table4 = []
            end_table5 = []
            #printTree(tree,0)

            #printTop()
            #printTop(bottomFiveCalculate(end_table,5))
            # Y_train[numbboard], table[4][-1][0],table[4][-1][1], table[4][-1][2][0], table[4][-1][2][1], table[4][-1][3][0], table[4][-1][3][0], table[4][-1][4][0], table[4][-1][4][1])
            time = stime.strftime("%H:%M:%S")
            #print("#%s Time: %s   Orig_Result: %s Pred_before_moves: %s Pred_after_moves: %s Area Score: %s"
            #      %(counter,time,initResult,outcome, table[4],table[2], ))
            #results.write("#%s Time: %s   Orig_Result: %s Pred_before_moves: %s Pred_after_moves: %s Area Score: %s  Other: %s/%s   %s/%s   %s/%s"%(counter,time,Y_train[numbboard],outcome, table[4][-1][0],table[4][-1][1], table[4][-1][2][0], table[4][-1][2][1], table[4][-1][3][0], table[4][-1][3][1], table[4][-1][4][0], table[4][-1][4][1]))
        else:
            #print("Invalid board: %s"%(counter))
            for i in range(5):
                counter[i] -= 1
            invalid_counter +=1
    timestamp3 = stime.strftime("%H:%M:%S")
    print("train Moves: %s " %(moves))
    print("Start Time        : %s " % (timestamp))
    print("Init finished Time: %s " % (timestamp2))
    print("Predict done Time : %s " % (timestamp3))
    results = open("Results/" + name + "/" + machine + "/" + machine + dim + loadfile + "tree" + sort + ".txt", 'a')
    for i in range(5):
        print("Moves: %s Total : %s/%s Loss: %s/%s Win: %s/%s Draw: %s/%s" % (i+1,counter_r[i],counter[i],lcounter_r[i],lcounter[i],wcounter_r[i],wcounter[i],dcounter_r[i],dcounter[i]))
        results.write("%s Moves: %s Total : %s/%s Loss: %s/%s Win: %s/%s Draw: %s/%s\n" % (
        sort, i + 1, counter_r[i], counter[i], lcounter_r[i], lcounter[i], wcounter_r[i], wcounter[i], dcounter_r[i],
        dcounter[i]))

        print("Invalid: %s" % (invalid_counter))
    #results.write("Start Time        : %s " % (timestamp))
    #results.write("Init finished Time: %s " % (timestamp2))
    #results.write("Predict done Time : %s " % (timestamp3))
    #results.write(counter_r,",",counter,lcounter_r,lcounter,wcounter_r,wcounter,dcounter_r,dcounter)
    print("\n")
    results.close()
def go_calc(board):
    board_size = 9
    komi = 7
    def play(_turn,game_board):
        x = _turn[1]
        y = _turn[2]
        color = _turn[0]
        game_board.play(x, y, color)
        return game_board
    def translate(board):
        _move_list = []
        for i in range(len(board)):
            x = i % 9
            y = i / 9
            y = str(int(y))
            y = y[0]
            y = int(y)
            if board[i] == "b" or board[i] == "B":
                _move = ["b", x, y]
                _move_list.append(_move)
            if board[i] == "w" or board[i] == "W":
                _move = ["w", x, y]
                _move_list.append(_move)
        return _move_list
    game_board = gomill.boards.Board(board_size)
    movelist = translate(board)
    for i in movelist:
        game_board = play(i,game_board)
    #area_score = game_board.area_score() - komi
    # print("Area Score:", area_score, "\n")
    # play(["b", 2,1])
    area_score = game_board.area_score() - komi
    # print("Area Score:", area_score, "\n")
    #print("------------------------------------------")
    #print(blackBoard)
    return area_score
for i in range(2):
    #main("test")
    main("train")