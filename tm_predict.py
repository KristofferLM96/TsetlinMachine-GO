import go_board_play as go_play
import numpy as np
import time as stime
#initialized with weights, clauses and tsetlin machine once.
#predictSum will need a black and white table with b . w
#will return prediction, score, area_score from go_board:play, loss, win and draw voters positive and negative.
#and will return a updated bitboard and a updated bwboard.

def init(_weights,_clauses, _tm,_weights2,_clauses2,_tm2):
    global weights, weights2,clauses,clauses2, btm,wtm, loss,win,draw,time,clause_count, clause_count2,wloss,wwin,wdraw
    weights = _weights
    weights2 = _weights2
    clauses = _clauses
    clauses2 = _clauses2
    btm = _tm
    wtm = _tm2
    loss = weights[0][0]
    win = weights[1][0]
    draw = weights[2][0]
    wloss= weights2[0][0]
    wwin= weights2[1][0]
    wdraw= weights2[2][0]
    time= 0
    clause_count = []
    clause_count2 = []
    go_play.setTime()
    for i in range(12):
        temp = []
        for j in range(clauses):
            temp.append(0)
        clause_count.append(temp)
    for i in range(12):
        temp = []
        for j in range(clauses2):
            temp.append(0)
        clause_count2.append(temp)

def getTime():
    time2 = go_play.getTime()
    return time, time2
def getClause():
    return clause_count, loss,win,draw
def getClause2():
    return clause_count2, wloss,wwin,wdraw
def predictSum(boards2, initResult, player):
    global time
    go_correct,nbwtable = go_play.go_calc(boards2)
    seconds = int(round(stime.time()))
    bittable = reform(nbwtable,9)
    newArray = np.array([bittable])
    if player == "W":
        result2 = wtm.transform(newArray,inverted = False)
        lossresult = weightedCalc2(result2[0][0:clauses2], wloss, 0, initResult)
        winresult = weightedCalc2(result2[0][clauses2:clauses2 * 2], wwin, 1, initResult)
        drawresult = weightedCalc2(result2[0][clauses2 * 2:clauses2 * 3], wdraw, 2, initResult)
    else:
        result2 = btm.transform(newArray, inverted=False)
        lossresult = weightedCalc(result2[0][0:clauses],loss,0, initResult)
        winresult = weightedCalc(result2[0][clauses:clauses*2], win,1, initResult)
        drawresult = weightedCalc(result2[0][clauses*2:clauses*3], draw,2, initResult)
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
    seconds2 = int(round(stime.time()))
    time += seconds2-seconds
    return outcome, score, go_correct, lossresult, winresult, drawresult,bittable,nbwtable
def weightedCalc(clause, weight,stat, initResult):
    negs = 0
    ones = 0
    for i in range(len(clause)):
        if clause[i] == 1:
            if i%2 == 0:
                ones += clause[i]*weight[i]
                if initResult == stat:
                    clause_count[stat][i]+=clause[i]
                else:
                    clause_count[stat+3][i] += clause[i]
            else:
                negs += clause[i]*weight[i]
                if initResult == stat:
                    clause_count[stat+6][i]+=clause[i]
                else:
                    clause_count[stat + 9][i] += clause[i]

    return ones,negs
def weightedCalc2(clause, weight,stat, initResult):
    negs = 0
    ones = 0
    for i in range(len(clause)):
        if clause[i] == 1:
            if i%2 == 0:
                ones += clause[i]*weight[i]
                if initResult == stat:
                    clause_count2[stat][i]+=clause[i]
                else:
                    clause_count2[stat+3][i] += clause[i]
            else:
                negs += clause[i]*weight[i]
                if initResult == stat:
                    clause_count2[stat+6][i]+=clause[i]
                else:
                    clause_count2[stat + 9][i] += clause[i]

    return ones,negs
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