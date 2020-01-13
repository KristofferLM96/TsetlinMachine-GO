from pyTsetlinMachineParallel.tm import MultiClassTsetlinMachine
import numpy as np
import csv
from time import time
import time as stime

def StartMachine(clauses,epoch,Threshold,S, inndata,dim):
    timestr = stime.strftime("%m%d-%H%M")
    results = open("Results/2D"+dim+timestr+".csv",'a')
    resultclauses = open("Results/2D"+dim+timestr+"clauses1.csv",'a')

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
    results.write("MultiClassTsetlinMachineParallel,2D,")
    while ecount < epoch:
        results.write("Epoch"+str(ecount+1)+",")
        ecount+=1
    results.write("\n")

    results.write(
        "Settings:\nClauses:,%.1f\nThreshold:,%.1f\nS:,%.1f\n" % (clauses, Threshold, S))
    while counter < 10:
        numb = str(counter)
        train_data = np.loadtxt("dataset/"+dim+inndata+numb+"train", delimiter=",")
        #train_data = np.loadtxt("dataset/test", delimiter=",")

        X_train = train_data[:, 0:-1]
        Y_train = train_data[:, -1]

        test_data = np.loadtxt("dataset/"+dim+inndata+numb+"test", delimiter=",")
        #test_data = np.loadtxt("dataset/test", delimiter=",")
        X_test = test_data[:, 0:-1]
        Y_test = test_data[:, -1]


        tm = MultiClassTsetlinMachine(clauses, Threshold, S, boost_true_positive_feedback=1, weighted_clauses=True)
        #tm.fit(X_train, Y_train, epochs=200)
        print("-------------------------------------------------------------------------------------------")
        print("MultiClassTsetlinMachine using %s%s%s writen to file %s.csv\n" %(dim,inndata,numb,timestr))
        print("Settings: Clauses: %.1f Threshold: %.1f S: %.1f\n" % (clauses, Threshold, S))
        print("\nAccuracy over 200 epochs:\n")

        results.write(dim+inndata + numb + ",")
        for i in range(epoch):
            start = time()
            tm.fit(X_train, Y_train, epochs=1, incremental=True)
            stop = time()
            timestamp = stime.strftime("%H:%M:%S")
            result = 100 * (tm.predict(X_test) == Y_test).mean()
            print("#%d Time: %s Accuracy: %.2f%% (%.2fs)" % (i + 1, timestamp, result, stop - start))
            #results.write("#%d Accuracy: %.2f%% (%.2fs)\n" % (i + 1, result, stop - start))
            results.write(",%.4f" % (np.mean(result)))
        results.write("\n")
        counter += 1
        print("Accuracy:", 100 * (tm.predict(X_test) == Y_test).mean())
        if(counter == 10):
            PrintClass(tm, 1, clauses)
            resultclauses.close()
            resultclauses = open("Results/2D"+dim + timestr + "clauses0.csv", 'a')
            PrintClass(tm, 0, clauses)
            resultclauses.close()
            if (inndata == "draw"):
                resultclauses = open("Results/2D"+dim + timestr + "clauses2.csv", 'a')
                PrintClass(tm, 2, clauses)
                resultclauses.close()
        #Align(tm, 1, clauses)


    print("Prediction: x1 = 1, x2 = 0, ... -> y = %d" % (tm.predict(np.array([[1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0]]))))
    print("Prediction: x1 = 0, x2 = 1, ... -> y = %d" % (tm.predict(np.array([[0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0]]))))
    print("Prediction: x1 = 0, x2 = 0, ... -> y = %d" % (tm.predict(np.array([[0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0]]))))
    print("Prediction: x1 = 1, x2 = 1, ... -> y = %d" % (tm.predict(np.array([[1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0]]))))
    #PrintClass(tm,1,clauses)
    #resultclauses.close()

    #resultclauses = open("2Dresults/2D"+timestr+"clauses.csv",'a')
    results.close()
def runner():
    # Settings
    clauses = 1000
    Threshold = 9000
    S = 27.0
    epoch = 30
    dim = "9x9"
    inndata = "nodraw"
    #StartMachine(clauses,epoch,Threshold,S,inndata)
    #StartMachine(clauses, epoch, Threshold, S, inndata)
    #StartMachine(clauses, epoch, 8800, S, inndata)
    #StartMachine(clauses, epoch, Threshold, S, "draw")
    #StartMachine(clauses,epoch,Threshold,S,inndata)
    StartMachine(clauses, epoch, Threshold, S, "nodraw","9x9")
    #StartMachine(clauses, epoch, Threshold, S, "nodraw")


runner()