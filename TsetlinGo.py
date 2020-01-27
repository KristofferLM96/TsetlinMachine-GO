from pyTsetlinMachineParallel.tm import MultiClassTsetlinMachine
from pyTsetlinMachineParallel.tm import MultiClassConvolutionalTsetlinMachine2D
import numpy as np
from statistics import mean
import csv
from time import time
import time as stime

def StartMachine(clauses,epoch,Threshold,S,inndata,dim,machine,Window_X,Window_Y,Shape_X,Shape_Y,Shape_Z,Name, Write_Clauses,kFold):
    timestr = stime.strftime("%m%d-%H%M")
    results = open("Results/"+Name+"/"+machine+"/"+machine+dim+timestr+".csv",'a')
    ecount = 0
    counter = 0
    if machine == "TM":
        results.write("MultiClassTsetlinMachineParallel,Parallel,")
    if machine == "cTM":
        results.write(
            "MultiClassConvolutionalTsetlinMachine2D,Parallel,")
    meanTab = []
    Highest = 0
    while ecount < epoch:
        results.write("Epoch"+str(ecount+1)+",")
        ecount+=1
        meanTab.append(0)
    results.write("\n")

    if machine =="TM": results.write(
        "Settings:\nClauses:,%.1f\nThreshold:,%.1f\nS:,%.1f\n" % (clauses, Threshold, S))
    if machine =="cTM": results.write(
        "Settings:\nClauses:,%.1f\nThreshold:,%.1f\nS:,%.1f\nWindow_X:,%.1f\nWindow_Y:,%.1f\nShape_X:,%.1f\nShape_Y:,%.1f\nShape_Z:,%.1f\n" % (
        clauses, Threshold, S, Window_X, Window_Y, Shape_X, Shape_Y, Shape_Z))

    while counter < kFold:
        numb = str(counter)
        global X_train,Y_train,X_test,Y_test,m
        train_data = np.loadtxt("Data/" + dim + inndata + numb + "train", delimiter=",")
        test_data = np.loadtxt("Data/" + dim + inndata + numb + "test", delimiter=",")
        if machine == "TM":
            X_train = train_data[:, 0:-1]
            Y_train = train_data[:, -1]
            X_test = test_data[:, 0:-1]
            Y_test = test_data[:, -1]
            m = MultiClassTsetlinMachine(clauses, Threshold, S, boost_true_positive_feedback=0, weighted_clauses=True)
            print("-------------------------------------------------------------------------------------------")
            print("MultiClassTsetlinMachine using %s%s%s writen to file %s.csv\n" %(dim,inndata,numb,timestr))
            print("Settings: Clauses: %.1f Threshold: %.1f S: %.1f\n" % (clauses, Threshold, S))
        if machine == "cTM":
            X_train = train_data[:, 0:-1].reshape(train_data.shape[0], Shape_X, Shape_Y, Shape_Z)
            Y_train = train_data[:, -1]
            X_test = test_data[:, 0:-1].reshape(test_data.shape[0], Shape_X, Shape_Y, Shape_Z)
            Y_test = test_data[:, -1]
            m = MultiClassConvolutionalTsetlinMachine2D(clauses, Threshold, S, (Window_X, Window_Y),boost_true_positive_feedback=0, weighted_clauses=True)
            print("-------------------------------------------------------------------------------------------")
            print("MultiClassConvolutionalTsetlinMachine2D using %s %s writen to file %s.csv (%.1f x %.1f x %.1f)\n" % (inndata, str(counter), timestr, Shape_X, Shape_Y, Shape_Z))
            print("Settings: Clauses: %.1f Threshold: %.1f S: %.1f Window_X: %.1f Window_Y: %.1f\n" % (clauses, Threshold, S, Window_X, Window_Y))

        results.write(dim+inndata + numb + ",")
        for i in range(epoch):
            start = time()
            m.fit(X_train, Y_train, epochs=1, incremental=True)
            stop = time()
            timestamp = stime.strftime("%H:%M:%S")
            start_testing = time()
            result = 100 * (m.predict(X_test) == Y_test).mean()
            stop_testing = time()
            print("#%d Time: %s Accuracy: %.2f%% Training: %.2fs Testing: %.2fs" % (i + 1, timestamp, result, stop - start,stop_testing-start_testing))
            meanTab[i] = meanTab[i] + result
            if Highest < result:
                Highest = result
            results.write(",%.4f" % (np.mean(result)))
        results.write("\n")
        counter += 1
        #print("Highest:", Highest)
        print("Accuracy:", 100 * (m.predict(X_test) == Y_test).mean())
        if(counter == Write_Clauses):
            WriteClauses(m, inndata, clauses,Shape_X, Shape_Y, Shape_Z, Window_X, Window_Y,machine, Name, dim, timestr)
    results.write("mean,")
    meancount=0
    meansepoch = 0
    highepoch = 0
    for i in meanTab:
        meancount+=1
        meansepoch += i/10
        if i/10 > highepoch:
            highepoch = i/10
        results.write(",%.4f" % (i/10))
    results.write(",%.4f" % (meansepoch / meancount))
    results.write("\n")
    results.write("Single/k-Fold")
    results.write(",%.4f" % (Highest))
    results.write(",%.4f" % (highepoch)) # should be highest epoch
    print("Highest: %.4f Highest k-Fold: %.4f Average k-Fold: %.4f" % (Highest, highepoch, meansepoch/meancount))
    results.close()
def runner():
    # Settings
    clauses = 4000
    Threshold = 16000
    S = 27.0
    epoch = 15
    dim = "9x9Natsukaze_"
    dim = "9x9Aya_"
    kFold = 10
    machine = "TM"    #cTM or TM
    #inndata = "Natsukaze_NoDraw"
    inndata = "Draw"
    Window_X = 7
    Window_Y = 7
    Shape_X = 9
    Shape_Y = 9
    Shape_Z = 2
    Name = "Trond"
    Write_Clauses = 0  #0 = don't print clauses, 1-10 which k-Fold to write clauses for.
    StartMachine(clauses, epoch, Threshold, S, inndata,dim,machine,Window_X,Window_Y,Shape_X,Shape_Y,Shape_Z,Name, Write_Clauses,kFold)
    StartMachine(8000, epoch, Threshold, S, inndata,dim,machine,Window_X,Window_Y,Shape_X,Shape_Y,Shape_Z,Name, Write_Clauses,kFold)
    StartMachine(16000, epoch, Threshold, S, inndata,dim,machine,Window_X,Window_Y,Shape_X,Shape_Y,Shape_Z,Name, Write_Clauses,kFold)


def WriteClauses(m, inndata, clauses,Shape_X, Shape_Y, Shape_Z, Window_X, Window_Y,machine, Name, dim, timestr):
    def TMGetOutput(tm,tm_class,clause):
        output = []
        for i in range(Shape_X*Shape_Y*4):
            outputbit = tm.ta_action(tm_class,clause,i)
            output.append(outputbit)
        return output
    def Align(tm,tm_class,clause):
        output =""
        if machine == "TM":
            output = TMGetOutput(tm,tm_class,clause)
        if machine == "cTM":
            output = cTMGetOutput(tm,tm_class,clause)
        nonNegated = output[:int(len(output)/2)]
        negated = output[int(len(output)/2):]
        xbit = (nonNegated[:int(len(nonNegated)/2)])
        obit = (nonNegated[int(len(nonNegated)/2):])
        nxbit = (negated[:int(len(negated)/2)])
        nobit = (negated[int(len(negated)/2):])
        board=[]
        for i in range(Shape_X*Shape_Y):
            resultclauses.write(str(xbit[i])+str(obit[i])+str(nxbit[i])+str(nobit[i]))
            if i < Shape_X*Shape_Y-1:
                resultclauses.write(",")
            else:
                resultclauses.write("\n")
    offset_y = Shape_Y - Window_Y
    offset_x = Shape_X - Window_X
    def cTMGetOutput(tm, tm_class, clause):
        output = []
        xyz_id_old = 0
        for y in range(Window_Y):
            for x in range(Window_X):
                for z in range(Shape_Z):
                    xyz_id = offset_y + offset_x + y * Shape_X * 2 + x * 2 + z
                    outputbit = tm.ta_action(tm_class, clause, xyz_id)
                    output.append(outputbit)
                    xyz_id_old = xyz_id + 1
        output = cTMGetOutNegated(tm, tm_class, clause, xyz_id_old, output)
        return output
    def cTMGetOutNegated(tm, tm_class, clause, xyz_id_old, output):
        for y in range(Window_Y):
            for x in range(Window_X):
                for z in range(Shape_Z):
                    xyz_id = xyz_id_old + offset_y + offset_x + y * Shape_X * 2 + x * 2 + z
                    outputbit = tm.ta_action(tm_class, clause, xyz_id)
                    output.append(outputbit)
        return output
    def PrintClass(Ts, Class, clauses):
        for i in range(clauses):
            Align(Ts, Class, i)
    resultclauses = open("Results/" + Name + "/" + machine + "/" + machine + dim + timestr + "clauses1.csv", 'a')
    PrintClass(m, 1, clauses)
    resultclauses.close()
    resultclauses = open("Results/" + Name + "/" + machine + "/" + machine + dim + timestr + "clauses0.csv", 'a')
    PrintClass(m, 0, clauses)
    resultclauses.close()
    if (inndata == "Draw"):
        resultclauses = open("Results/" + Name + "/" + machine + "/" + machine + dim + timestr + "clauses2.csv", 'a')
        PrintClass(m, 2, clauses)
        resultclauses.close()
runner()
