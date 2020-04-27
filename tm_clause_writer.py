from pyTsetlinMachineParallel.tm import MultiClassTsetlinMachine
from pyTsetlinMachineParallel.tm import MultiClassConvolutionalTsetlinMachine2D
import numpy as np
import time as stime
import tm_predict as predict
import go_board_play as go_board
machine = "TM"
name = "Trond"
dim = "90_100T_9x9Aya_"
loadfile = "0310-1342"
inndata = "Draw"
numb = "0"
###################
#numbboard = 654
#numbboard = 566
#numbboard = 868
numbboard = 91
depth = 3   #number of moves
tree_width = 3
#save_file = "91-5-4"
save_file = "-"

def init(machine):
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
    return m
def GetOutput(tm,tm_class,clause):
    output = []
    for i in range(162*2):
        outputbit = tm.ta_action(tm_class,clause,i)
        output.append(outputbit)
    return output
def Align(tm,tm_class,clause):
    output = GetOutput(tm,tm_class,clause)
    nonNegated = output[:int(len(output)/2)]
    negated = output[int(len(output)/2):]
    xbit = (nonNegated[:int(len(nonNegated)/2)])
    obit = (nonNegated[int(len(nonNegated)/2):])
    nxbit = (negated[:int(len(negated)/2)])
    nobit = (negated[int(len(negated)/2):])
    board=[]
    for i in range(81):
        resultclauses.write(str(xbit[i])+str(obit[i])+str(nxbit[i])+str(nobit[i]))
        if i < 80:
            resultclauses.write(",")
        else:
            resultclauses.write("\n")
def PrintClass(Ts,Class,clauses):
    for i in range(clauses):
        Align(Ts,Class,i)
        #resultclauses.writelines(clausesres)
        #print(clausesres)
        #PrintClause(action)

def main():
    global resultclauses
    clauses = 1000
    tm = init(machine)
    resultclauses = open("Results/" + name + "/" + machine + "/" + machine + dim + loadfile + save_file+"clauses1.csv", 'a')
    PrintClass(tm, 1, clauses)
    resultclauses.close()
    resultclauses = open("Results/" + name + "/" + machine + "/" + machine + dim + loadfile + save_file+"clauses0.csv", 'a')
    PrintClass(tm, 0, clauses)
    resultclauses.close()
    resultclauses = open("Results/" + name + "/" + machine + "/" + machine + dim + loadfile + save_file+"clauses2.csv", 'a')
    PrintClass(tm, 2, clauses)
    resultclauses.close()
main()