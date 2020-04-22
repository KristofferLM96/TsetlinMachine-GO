import go_board_play as go_play
import numpy as np
#initialized with weights, clauses and tsetlin machine once.
#predictSum will need a black and white table with b . w
#will return prediction, score, area_score from go_board:play, loss, win and draw voters positive and negative.
#and will return a updated bitboard and a updated bwboard.

def init(_weights,_clauses, _tm):
    global weights,clauses, tm, loss,win,draw
    weights = _weights
    clauses = _clauses
    tm = _tm
    loss = weights[0][0]
    win = weights[1][0]
    draw = weights[2][0]

def predictSum(boards2):
    go_correct,nbwtable = go_play.go_calc(boards2)
    bittable = reform(nbwtable,9)
    newArray = np.array([bittable])
    result2 = tm.transform(newArray,inverted = False)
    lossresult = weightedCalc(result2[0][0:clauses],loss)
    winresult = weightedCalc(result2[0][clauses:clauses*2], win)
    drawresult = weightedCalc(result2[0][clauses*2:clauses*3], draw)
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
    return outcome, score, go_correct, lossresult, winresult, drawresult,bittable,nbwtable
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