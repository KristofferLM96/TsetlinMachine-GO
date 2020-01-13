from pyTsetlinMachineParallel.tm import MultiClassTsetlinMachine
from pyTsetlinMachineParallel.tm import MultiClassConvolutionalTsetlinMachine2D
import numpy as np
import csv
from time import time
import time as stime

def StartMachine(clauses,epoch,Threshold,S,inndata,dim,machine,Window_X,Window_Y,Shape_X,Shape_Y,Shape_Z,Name):
    timestr = stime.strftime("%m%d-%H%M")
    results = open("Results/"+Name+"/"+machine+"/"+machine+dim+timestr+".csv",'a')
    resultclauses = open("Results/"+Name+"/"+machine+"/"+machine+dim+timestr+"clauses1.csv",'a')

    def GetOutput(tm,tm_class,clause):
        output = []
        for i in range(84*2):
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
        for i in range(42):
            resultclauses.write(str(xbit[i])+str(obit[i])+str(nxbit[i])+str(nobit[i]))
            if i < 41:
                resultclauses.write(",")
            else:
                resultclauses.write("\n")

    def PrintClass(Ts,Class,clauses):
        for i in range(clauses):
            Align(Ts,Class,i)
            #resultclauses.writelines(clausesres)
            #print(clausesres)
            #PrintClause(action)
    ecount = 0
    counter = 0
    if machine == "TM":
        results.write("MultiClassTsetlinMachineParallel,Parallel,")
    if machine == "cTM":
        results.write(
            "MultiClassConvolutionalTsetlinMachine2D,Parallel,")
    while ecount < epoch:
        results.write("Epoch"+str(ecount+1)+",")
        ecount+=1
    results.write("\n")

    if machine =="TM": results.write(
        "Settings:\nClauses:,%.1f\nThreshold:,%.1f\nS:,%.1f\n" % (clauses, Threshold, S))
    if machine =="cTM": results.write(
        "Settings:\nClauses:,%.1f\nThreshold:,%.1f\nS:,%.1f\nWindow_X:,%.1f\nWindow_Y:,%.1f\nShape_X:,%.1f\nShape_Y:,%.1f\nShape_Z:,%.1f\n" % (
        clauses, Threshold, S, Window_X, Window_Y, Shape_X, Shape_Y, Shape_Z))

    while counter < 10:
        numb = str(counter)
        global X_train,Y_train,X_test,Y_test,m
        train_data = np.loadtxt("dataset/" + dim + inndata + numb + "train", delimiter=",")
        test_data = np.loadtxt("dataset/" + dim + inndata + numb + "test", delimiter=",")
        #tm.fit(X_train, Y_train, epochs=200)
        if machine == "TM":
            X_train = train_data[:, 0:-1]
            Y_train = train_data[:, -1]
            X_test = test_data[:, 0:-1]
            Y_test = test_data[:, -1]
            m = MultiClassTsetlinMachine(clauses, Threshold, S, boost_true_positive_feedback=1, weighted_clauses=True)
            print("-------------------------------------------------------------------------------------------")
            print("MultiClassTsetlinMachine using %s%s%s writen to file %s.csv\n" %(dim,inndata,numb,timestr))
            print("Settings: Clauses: %.1f Threshold: %.1f S: %.1f\n" % (clauses, Threshold, S))
        if machine == "cTM":
            X_train = train_data[:, 0:-1].reshape(train_data.shape[0], Shape_X, Shape_Y, Shape_Z)
            Y_train = train_data[:, -1]
            X_test = test_data[:, 0:-1].reshape(test_data.shape[0], Shape_X, Shape_Y, Shape_Z)
            Y_test = test_data[:, -1]
            m = MultiClassConvolutionalTsetlinMachine2D(clauses, Threshold, S, (Window_X, Window_Y),boost_true_positive_feedback=1, weighted_clauses=True)
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
            results.write(",%.4f" % (np.mean(result)))
        results.write("\n")
        counter += 1
        print("Accuracy:", 100 * (m.predict(X_test) == Y_test).mean())
        if(counter == 10):
            PrintClass(m, 1, clauses)
            resultclauses.close()
            resultclauses = open("Results/"+Name+"/"+machine+"/"+machine+dim + timestr + "clauses0.csv", 'a')
            PrintClass(m, 0, clauses)
            resultclauses.close()
            if (inndata == "draw"):
                resultclauses = open("Results/"+Name+"/"+machine+"/"+machine+dim + timestr + "clauses2.csv", 'a')
                PrintClass(m, 2, clauses)
                resultclauses.close()
        #Align(tm, 1, clauses)
    print("Prediction: x1 = 1, x2 = 0, ... -> y = %d" % (m.predict(np.array([[1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0]]))))
    print("Prediction: x1 = 0, x2 = 1, ... -> y = %d" % (m.predict(np.array([[0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0]]))))
    print("Prediction: x1 = 0, x2 = 0, ... -> y = %d" % (m.predict(np.array([[0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0]]))))
    print("Prediction: x1 = 1, x2 = 1, ... -> y = %d" % (m.predict(np.array([[1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0]]))))
    #PrintClass(tm,1,clauses)
    #resultclauses.close()
    #resultclauses = open("2Dresults/2D"+timestr+"clauses.csv",'a')
    results.close()
def runner():
    # Settings
    clauses = 100
    Threshold = 800
    S = 27.0
    epoch = 20
    dim = "9x9"
    machine = "cTM"    #cTM or TM
    inndata = "nodraw"
    Window_X = 4
    Window_Y = 4
    Shape_X = 9
    Shape_Y = 9
    Shape_Z = 2
    Name = "Trond"
    StartMachine(clauses, epoch, Threshold, S, inndata,dim,machine,Window_X,Window_Y,Shape_X,Shape_Y,Shape_Z,Name)
runner()