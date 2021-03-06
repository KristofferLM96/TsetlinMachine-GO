from pyTsetlinMachineParallel.tm import MultiClassTsetlinMachine
from pyTsetlinMachineParallel.tm import MultiClassConvolutionalTsetlinMachine2D
import numpy as np
import time as stime
import operator
import tm_predict as predict
weights = []
clauses= 0
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
#numbboard = 388
#######################
depth = 7   #number of moves 5,7,9
tree_width = 2
save_name = "train7"
#######################
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
            print(table)
            print(i)
            print(table[i])
    return black+white

def moveTransform(number,size): #change the moves into letter/number variation
    if(number < 0): return "Start     "
    Alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
    a = int(number/size)
    b = number%size
    return alphabet[b]+str(size-a)+"        "
def findEmpty(table, player,size, width, initResult):
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
            outcome, score, go_outcome, lossresult, winresult, drawresult, retTable, retBw = predict.predictSum(tempTable2, initResult, player)
            #newM = tableCopy(table[2])
            newM = go_outcome
            #newP = tableCopy(table[3])
            #newO = tableCopy(table[4])
            #newS = tableCopy(table[5])
            newP=player
            newO=outcome
            newS =score
            alteredTables.append([retTable,retBw,newM,newP, newO, newS,lossresult,winresult,drawresult])
    #print(alteredTables)
    #Y_train[numbboard], table[4][-1][0],table[4][-1][1], table[4][-1][2][0], table[4][-1][2][1], table[4][-1][3][0], table[4][-1][3][0], table[4][-1][4][0], table[4][-1][4][1])
    alteredTables = topFive(alteredTables,player, width)
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
end_table6 = []
end_table7 = []
end_table8 = []
end_table9 = []
def recursive(bwtable,player,size,moves,tot, width, initResult):
    if tot == 9:
        if moves == 0: end_table9.append(bwtable)
        if moves == 1: end_table8.append(bwtable)
        if moves == 2: end_table7.append(bwtable)
        if moves == 3: end_table6.append(bwtable)
        if moves == 4: end_table5.append(bwtable)
        if moves == 5: end_table4.append(bwtable)
        if moves == 6: end_table3.append(bwtable)
        if moves == 7: end_table2.append(bwtable)
        if moves == 8: end_table1.append(bwtable)
    if tot == 7:
        if moves == 0: end_table7.append(bwtable)
        if moves == 1: end_table6.append(bwtable)
        if moves == 2: end_table5.append(bwtable)
        if moves == 3: end_table4.append(bwtable)
        if moves == 4: end_table3.append(bwtable)
        if moves == 5: end_table2.append(bwtable)
        if moves == 6: end_table1.append(bwtable)
    if tot == 5:
        if moves == 0: end_table5.append(bwtable)
        if moves == 1: end_table4.append(bwtable)
        if moves == 2: end_table3.append(bwtable)
        if moves == 3: end_table2.append(bwtable)
        if moves == 4: end_table1.append(bwtable)
        if moves == 0: return bwtable
    if moves == 0: return bwtable
    moves -= 1
    newBoards = findEmpty(bwtable,player,size, width, initResult)
    for i in newBoards:
        if i[3][-1] == "B":
            nplayer = "W"
        else:
            nplayer = "B"
        i.append(recursive(i, nplayer, size, moves,tot, width, initResult))
    bwtable.append(newBoards)

    #bwtable[0] have bitboard
    #bwtable[1] have black/white table
    #bwtable[2] have go_outcome,
    #bwtable[3] have player
    #bwtable[4] have outcome
    #bwtable[5] have score make as table? tmscore = index 0 go score =index 1 or vice versa
    #bwtable[6] have loss
    #bwtable[7] have win
    #bwtable[8] have draw
    #bwtable[9] have list of top5 children nodes (newBoards)
    return bwtable

def topFive(boards, player, width):
    number = width #how wide is the search
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
def topFiveCalculate(boards, numb):
    listallscore = []
    list =[]
    for i in range(numb):
        tempScore = -100000
        tempID = 0
        for j in range(len(boards)):
            listallscore.append(boards[j][5])
            #if abs(boards[j][5][0]) > tempScore:
            if boards[j][5] > tempScore:
                #tempScore = abs(boards[j][5][0])
                tempScore = boards[j][5]
                tempID = j
            if boards[j][5] == tempScore:
                np.random.seed()
                X1 = np.random.randint(low=0, high=10, size=(1))
                if X1[0] > 4:
                    tempScore = boards[j][5]
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
            listallscore.append(boards[j][5])
            #if abs(boards[j][5][0]) < tempScore:
                #tempScore = abs(boards[j][5][0])
            if boards[j][5] < tempScore:
                tempScore = boards[j][5]
                tempID = j
            if boards[j][5] == tempScore:
                np.random.seed()
                X1 = np.random.randint(low=0, high=10, size=(1))
                if X1[0] > 4:
                    tempScore = boards[j][5]
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
def main(sort,moves,width):
    global end_table1,end_table2,end_table3,end_table4,end_table5,end_table6,end_table7,end_table8,end_table9
    #moves = 7
    results = open("Results/" + name + "/" + machine + "/" + machine + dim + loadfile + "tree"+sort+".txt", 'a')
    results.close()
    results1 = open("Results/" + name + "/" + machine + "/" + machine + dim + loadfile + "detai_" + sort + ".csv", 'a')
    # print("orig_result")
    results1.write("orig_result")
    for i in range(10):
        results1.write(",%s_loss_pro,%s_loss_neg,%s_win_pro,%s_win_neg,%s_draw_pro,%s_draw_neg,%s_area_score" % (i, i, i, i, i, i,i))
        # print(",%s_loss_pro,%s_loss_neg,%s_win_pro,%s_win_neg,%s_draw_pro,%s_draw_neg,"%(i,i,i,i,i,i))
        #results1.write(("area_score"))
        # print("area_score")
    results1.write("\n")
    results1.close()
    results2 = open("Results/" + name + "/" + machine + "/" + machine + dim + loadfile + "short_" + sort + ".csv", 'a')
    # print("orig_result")
    results2.write("orig_result")
    for i in range(10):
        # print(",%s_area,%s_result,%s_score"%(i,i,i))
        results2.write(",%s_area,%s_result,%s_score" % (i, i, i))
    results2.write("\n")
    results2.close()
    timestamp = stime.strftime("%H:%M:%S")
    print("Start Time        : %s " % (timestamp))
    numb = "0"
    init(dim,machine,loadfile,numb)
    predict.init(weights,clauses,m,m)
    timestamp2 = stime.strftime("%H:%M:%S")
    print("Init finished Time: %s " % (timestamp2))
    invalid_counter = 0
    counter = [0,0,0,0,0,0,0,0,0]
    wcounter = [0,0,0,0,0,0,0,0,0]
    lcounter = [0,0,0,0,0,0,0,0,0]
    dcounter = [0,0,0,0,0,0,0,0,0]
    counter_r = [0,0,0,0,0,0,0,0,0]
    wcounter_r = [0,0,0,0,0,0,0,0,0]
    lcounter_r = [0,0,0,0,0,0,0,0,0]
    dcounter_r = [0,0,0,0,0,0,0,0,0]
    print(len(X_test))
    print(len(X_train))
    printnumb = 1 #1
    printnumb2 = 1#1
    for numbboard in range(1004): #10063 #1004
        #numbboard+=1
        #numbboard+=40000
        #print(numbboard)
        if (counter[0] == printnumb2 * 10):
            tempTime = stime.strftime("%H:%M:%S")
            print("Time: %s Done: %s Total: %s" % (tempTime, printnumb2 * 10, 1000))
            for i in range(9):
                print("Moves: %s Total : %s/%s Loss: %s/%s Win: %s/%s Draw: %s/%s" % (i+1,
                    counter_r[i], counter[i], lcounter_r[i], lcounter[i], wcounter_r[i], wcounter[i], dcounter_r[i],
                    dcounter[i]))
            print("Invalid board: %s" % (invalid_counter))
            printnumb2 += 1
        if(counter[0] == printnumb*100):
            tempTime = stime.strftime("%H:%M:%S")
            print("Time: %s Done: %s Total: %s"%(tempTime,printnumb*100,1000))
            results = open("Results/" + name + "/" + machine + "/" + machine + dim + loadfile + "tree" + sort + ".txt",
                           'a')
            results.write("Time: %s Done: %s Total: %s\n"%(tempTime,printnumb*100,10000))
            for i in range(9):
                print("Moves: %s Total : %s/%s Loss: %s/%s Win: %s/%s Draw: %s/%s" % (i+1,
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
        for i in range(9):
            counter[i]+=1
        initBoard = X_train[numbboard]
        initResult = Y_train[numbboard]
        if sort == "test":
            initBoard = X_test[numbboard]
            initResult = Y_test[numbboard]

        if sum(initBoard) < 73 and initResult != 2:
            newArray = np.array([initBoard])
            bwtable = transform(initBoard, size)
            table6 = []
            table7 = []
            table8 = []
            table9 = []
            outcome, score, percentage, losstot,wintot,drawtot, newbit,newbw = predict.predictSum(bwtable, initResult, player)
            bwTable = [initBoard,bwtable, percentage, player, outcome, score]
            tree = recursive(bwTable, player, size, moves,moves, width, initResult)
            fivetable1 = topFive(end_table1,"B", width)
            table1 = fivetable1[0]
            fivetable2 = topFive(end_table2, "W", width)
            table2 = fivetable2[0]
            fivetable3 = topFive(end_table3, "B", width)
            table3 = fivetable3[0]
            fivetable4 = topFive(end_table4, "W", width)
            table4 = fivetable4[0]
            fivetable5 = topFive(end_table5, "B", width)
            table5 = fivetable5[0]
            if moves > 5:
                fivetable6 = topFive(end_table6, "W", width)
                table6 = fivetable6[0]
                fivetable7 = topFive(end_table7, "B", width)
                table7 = fivetable7[0]
            else:
                table6 = [0, 0, 0, 0, 0, 0, 0, 0]
                table7 = [0, 0, 0, 0, 0, 0, 0, 0]
            if moves >7:
                fivetable8 = topFive(end_table8, "W", width)
                table8 = fivetable8[0]
                fivetable9 = topFive(end_table9, "B", width)
                table9 = fivetable9[0]
            else:
                table8 = [0, 0, 0, 0, 0, 0, 0, 0]
                table9 = [0, 0, 0, 0, 0, 0, 0, 0]

            if initResult == 0:
                for i in range(9):
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
                if table6[2] < 0:
                    lcounter_r[5]+=1
                    counter_r[5] +=1
                if table7[2] < 0:
                    lcounter_r[6]+=1
                    counter_r[6] +=1
                if table8[2] < 0:
                    lcounter_r[7]+=1
                    counter_r[7] +=1
                if table9[2] < 0:
                    lcounter_r[8]+=1
                    counter_r[8] +=1
            elif initResult == 1:
                for i in range(9):
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
                if table6[2] > 0:
                    wcounter_r[5]+=1
                    counter_r[5] +=1
                if table7[2] > 0:
                    wcounter_r[6]+=1
                    counter_r[6] +=1
                if table8[2] > 0:
                    wcounter_r[7]+=1
                    counter_r[7] +=1
                if table9[2] > 0:
                    wcounter_r[8]+=1
                    counter_r[8] +=1
            else:
                for i in range(9):
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
                if table6[2] == 0:
                    dcounter_r[5]+=1
                    counter_r[5] +=1
                if table7[2] == 0:
                    dcounter_r[6]+=1
                    counter_r[6] +=1
                if table8[2] == 0:
                    dcounter_r[7]+=1
                    counter_r[7] +=1
                if table9[2] == 0:
                    dcounter_r[8]+=1
                    counter_r[8] +=1
            end_table1 = []
            end_table2 = []
            end_table3 = []
            end_table4 = []
            end_table5 = []
            end_table6 = []
            end_table7 = []
            end_table8 = []
            end_table9 = []
            #printTree(tree,0)
            # print(initResult,)
            results1 = open(
                "Results/" + name + "/" + machine + "/" + machine + dim + loadfile + "detai_" + sort + ".csv", 'a')
            # print("%s,%s,%s,%s,%s,%s,%s"%(initResult,losstot[0],losstot[1], wintot[0],wintot[1],drawtot[0],drawtot[1]))
            results1.write("%s,%s,%s,%s,%s,%s,%s,%s" % (
            initResult, losstot[0], losstot[1], wintot[0], wintot[1], drawtot[0], drawtot[1],percentage))
            # print(",%s,%s,%s,%s,%s,%s"%(table[6][0],table[6][1],table[7][0],table[7][1],table[8][0],table[8][1],table[2]))
            results1.write(",%s,%s,%s,%s,%s,%s,%s" % (
            table1[6][0], table1[6][1], table1[7][0], table1[7][1], table1[8][0], table1[8][1], table1[2]))
            results1.write(
                ",%s,%s,%s,%s,%s,%s,%s" % (
                table2[6][0], table2[6][1], table2[7][0], table2[7][1], table2[8][0], table2[8][1], table2[2]))
            results1.write(
                ",%s,%s,%s,%s,%s,%s,%s" % (
                table3[6][0], table3[6][1], table3[7][0], table3[7][1], table3[8][0], table3[8][1], table3[2]))
            results1.write(
                ",%s,%s,%s,%s,%s,%s,%s" % (
                table4[6][0], table4[6][1], table4[7][0], table4[7][1], table4[8][0], table4[8][1], table4[2]))
            results1.write(
                ",%s,%s,%s,%s,%s,%s,%s" % (
                table5[6][0], table5[6][1], table5[7][0], table5[7][1], table5[8][0], table5[8][1], table5[2]))
            #results1.write(
            #    ",%s,%s,%s,%s,%s,%s,%s" % (
            #        table6[6][0], table6[6][1], table6[7][0], table6[7][1], table6[8][0], table6[8][1], table6[2]))
            #results1.write(
            #    ",%s,%s,%s,%s,%s,%s,%s" % (
            #        table7[6][0], table7[6][1], table7[7][0], table7[7][1], table7[8][0], table7[8][1], table7[2]))
            #results1.write(
            #    ",%s,%s,%s,%s,%s,%s,%s" % (
            #        table8[6][0], table8[6][1], table8[7][0], table8[7][1], table8[8][0], table8[8][1], table8[2]))
            #results1.write(
            #    ",%s,%s,%s,%s,%s,%s,%s" % (
            #        table9[6][0], table9[6][1], table9[7][0], table9[7][1], table9[8][0], table9[8][1], table9[2]))
            results1.write("\n")
            results1.close()

            results2 = open(
                "Results/" + name + "/" + machine + "/" + machine + dim + loadfile + "short_" + sort + ".csv", 'a')
            # print(initResult,percentage,outcome,score)
            results2.write("%s,%s,%s,%s" % (initResult, percentage, outcome, score))
            #for i in range(9):
                # print(table[2], table[4], table[5])
            results2.write(",%s,%s,%s" % (table1[2], table1[4], table1[5]))
            results2.write(",%s,%s,%s" % (table2[2], table2[4], table2[5]))
            results2.write(",%s,%s,%s" % (table3[2], table3[4], table3[5]))
            results2.write(",%s,%s,%s" % (table4[2], table4[4], table4[5]))
            results2.write(",%s,%s,%s" % (table5[2], table5[4], table5[5]))
            results2.write(",%s,%s,%s" % (table6[2], table6[4], table6[5]))
            results2.write(",%s,%s,%s" % (table7[2], table7[4], table7[5]))
            results2.write(",%s,%s,%s" % (table8[2], table8[4], table8[5]))
            results2.write(",%s,%s,%s" % (table9[2], table9[4], table9[5]))
            results2.write("\n")
            results2.close()
            #printTop()
            #printTop(bottomFiveCalculate(end_table,5))
            # Y_train[numbboard], table[4][-1][0],table[4][-1][1], table[4][-1][2][0], table[4][-1][2][1], table[4][-1][3][0], table[4][-1][3][0], table[4][-1][4][0], table[4][-1][4][1])
            time = stime.strftime("%H:%M:%S")
            #print("#%s Time: %s   Orig_Result: %s Pred_before_moves: %s Pred_after_moves: %s Area Score: %s  Other: %s/%s   %s/%s   %s/%s"%
            #      (counter,time,initResult,outcome, table[4],table[4][-1][1], table[4][-1][2][0], table[4][-1][2][1], table[4][-1][3][0], table[4][-1][3][1], table[4][-1][4][0], table[4][-1][4][1]))
#)
            #results.write("#%s Time: %s   Orig_Result: %s Pred_before_moves: %s Pred_after_moves: %s Area Score: %s  Other: %s/%s   %s/%s   %s/%s"%(counter,time,Y_train[numbboard],outcome, table[4][-1][0],table[4][-1][1], table[4][-1][2][0], table[4][-1][2][1], table[4][-1][3][0], table[4][-1][3][1], table[4][-1][4][0], table[4][-1][4][1]))
        else:
            #print("Invalid board: %s"%(counter))
            for i in range(9):
                counter[i] -= 1
            invalid_counter +=1
    timestamp3 = stime.strftime("%H:%M:%S")
    print("train Moves: %s " %(moves))
    print("Start Time        : %s " % (timestamp))
    print("Init finished Time: %s " % (timestamp2))
    print("Predict done Time : %s " % (timestamp3))
    results = open("Results/" + name + "/" + machine + "/" + machine + dim + loadfile + "tree" + sort + ".txt", 'a')
    for i in range(9):
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


main(save_name,depth,tree_width)
resul = open("Results/" + name + "/" + machine + "/" + machine + dim + loadfile + save_name+ "clauses"+".csv", 'a')
claus,losses,wins,draws = predict.getClause()
resul.write("loss,win,draw - pos_true, pos_false, neg_true, neg_false")
for i in range(12):
    for j in range(1000):
        resul.write("%s,"%(claus[i][j]))
    resul.write("\n")
resul.write("Weights:")
for j in range(1000):
    resul.write("%s,"%(losses[j]))
resul.write("\n")
for j in range(1000):
    resul.write("%s,"%(wins[j]))
resul.write("\n")
for j in range(1000):
    resul.write("%s,"%(draws[j]))
resul.write("\n")
resul.close()
#loss pos
#win pos
#draw pos
#loss neg
#win neg
#draw neg

def tempMain():
    init(dim, machine, loadfile, "0")
    results = open("Results/" + name + "/" + machine + "/" + machine + dim + loadfile + "notworking"+".txt", 'a')
    for numbboard in range(1004):  # 10063
        initBoard = X_train[numbboard]
        if sum(initBoard) > 72:
            results.write("%s \n"%(numbboard))
    results.close()
#tempMain()    if nbwtable != boards2:
