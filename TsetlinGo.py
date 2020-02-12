from pyTsetlinMachineParallel.tm import MultiClassTsetlinMachine
from pyTsetlinMachineParallel.tm import MultiClassConvolutionalTsetlinMachine2D
import numpy as np
from time import time
import time as stime

def StartMachine(clauses,epoch,Threshold,S,inndata,dim,machine,Window_X,Window_Y,Shape_X,Shape_Y,Shape_Z,Name, Write_Clauses,kFold,savestate,loadstate,loadfile):
    timestr = stime.strftime("%m%d-%H%M")
    results = open("Results/"+Name+"/"+machine+"/"+machine+dim+timestr+".csv",'a')
    ecount = 0
    counter = 0
    resArray =[]

    if loadstate == 1:
        with open("Results/" + "Trond" + "/" + "TM" + "/" + machine+dim+loadfile+".csv", 'r') as file:
            loadarray = []
            for line in file.readlines():
                # print(line)
                lineds = [str(x) for x in line.strip().split(',')]
                # print (lineds)
                # linesd = str(lineds[0])
                if lineds[-1] == "":
                    loadarray.append(lineds[:-1])
                else:
                    loadarray.append(lineds)
            if loadarray[0][0][10] == "T":
                machine = "TM"
            else:
                machine = "cTM"
            kFoldstart = 0
            clauses = int(loadarray[2][1][:-2])
            Threshold = int(loadarray[3][1][:-2])
            S = int(loadarray[4][1][:-2])
            if machine == "TM":
                kFoldstart = 5
            if machine == "cTM":
                Window_X = int(loadarray[5][1][:-2])
                Window_Y = int(loadarray[6][1][:-2])
                Shape_X = int(loadarray[7][1][:-2])
                Shape_Y = int(loadarray[8][1][:-2])
                Shape_Z = int(loadarray[9][1][:-2])
                kFoldstart = 10
            # print(loadarray)
            #print(len(loadarray) - kFoldstart)

            resArray = []
            if (len(loadarray) - kFoldstart > 10):
                for i in range(len(loadarray) - kFoldstart - 2):
                    resArray.append(loadarray[i + kFoldstart][2:])
            else:
                for i in range(len(loadarray) - kFoldstart):
                    resArray.append(loadarray[i + kFoldstart][2:])
            #print(resArray)

    if machine == "TM":
        results.write("MultiClassTsetlinMachineParallel,Parallel")
    if machine == "cTM":
        results.write(
            "MultiClassConvolutionalTsetlinMachine2D,Parallel")
    meanTab = []
    Highest = 0
    while ecount < epoch:
        results.write(","+"Epoch"+str(ecount+1))
        ecount+=1
        meanTab.append(0)
    results.write("\n")

    if machine =="TM": results.write(
        "Settings:\nClauses:,%.1f\nThreshold:,%.1f\nS:,%.1f\n" % (clauses, Threshold, S))
    if machine =="cTM": results.write(
        "Settings:\nClauses:,%.1f\nThreshold:,%.1f\nS:,%.1f\nWindow_X:,%.1f\nWindow_Y:,%.1f\nShape_X:,%.1f\nShape_Y:,%.1f\nShape_Z:,%.1f\n" % (
        clauses, Threshold, S, Window_X, Window_Y, Shape_X, Shape_Y, Shape_Z))
    while counter < kFold:
        kFoldtotal = 0
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
        results.close()
        results = open("Results/" + Name + "/" + machine + "/" + machine + dim + timestr + ".csv", 'a')
        results.write(dim+inndata + numb + ",")
        results.close()
        startepoch = 1
        if loadstate == 1 and len(resArray) >= counter+1:
            #print(len(resArray))
            loadedstate = np.load("Results/" + Name + "/" + machine + "/" + machine + dim + loadfile +"kFold"+str(counter) + ".npy", allow_pickle=True)
            m.fit(X_train, Y_train, epochs=0, incremental=True)
            m.set_state(loadedstate)
            for i in range(len(resArray[counter])):
                loadresult = float(resArray[counter][i])
                timestamp = stime.strftime("%H:%M:%S")
                print("#%d Time: %s Accuracy: %.2f%% --loaded--" % (startepoch, timestamp, loadresult))
                startepoch += 1
                results = open("Results/" + Name + "/" + machine + "/" + machine + dim + timestr + ".csv", 'a')
                results.write(",%.4f" % (loadresult))
                kFoldtotal+=loadresult
                meanTab[i] = meanTab[i] + loadresult
                if Highest < loadresult:
                    Highest = loadresult
                if (savestate == 2 or savestate == 1):
                    x = m.get_state()
                    np.save("Results/" + Name + "/" + machine + "/" + machine + dim + timestr + "kFold" + str(
                        counter) + ".npy", x)
        #print(meanTab)
        startepoch-=1
        results.close()
        for i in range(epoch-startepoch):
            start = time()
            m.fit(X_train, Y_train, epochs=1, incremental=True)
            stop = time()
            timestamp = stime.strftime("%H:%M:%S")
            start_testing = time()
            result = 100 * (m.predict(X_test) == Y_test).mean()
            stop_testing = time()
            print("#%d Time: %s Accuracy: %.2f%% Training: %.2fs Testing: %.2fs" % (startepoch +i+1, timestamp, result, stop - start,stop_testing-start_testing))
            meanTab[i+startepoch] = meanTab[i+startepoch] + result
            if Highest < result:
                Highest = result
            if (savestate == 2):
                x = m.get_state()
                np.save("Results/" + Name + "/" + machine + "/" + machine + dim + timestr + "kFold" + str(counter) + ".npy",x)
            results = open("Results/" + Name + "/" + machine + "/" + machine + dim + timestr + ".csv", 'a')
            results.write(",%.4f" % (np.mean(result)))
            kFoldtotal += np.mean(result)
            results.close()
        results = open("Results/" + Name + "/" + machine + "/" + machine + dim + timestr + ".csv", 'a')
        results.write("\n")
        results.close()
        if(savestate == 1):
            x = m.get_state()
            np.save("Results/" + Name + "/" + machine + "/" + machine + dim + timestr +"kFold"+str(counter) + ".npy", x)
        counter += 1
        #print("Highest:", Highest)
        meancount = 0
        meansepoch = 0
        highepoch = 0
        for i in meanTab:
            meancount += 1
            meansepoch += i / counter
            if i / counter > highepoch:
                highepoch = i / counter
        print("Average Epoch: %.4f " % (kFoldtotal/meancount))
        print("Total Highest: %.4f Total Highest k-Fold: %.4f Total Average k-Fold: %.4f" % (
            Highest, highepoch, meansepoch / meancount))
        #print("Accuracy:", 100 * (m.predict(X_test) == Y_test).mean())
        if(counter == Write_Clauses):
            WriteClauses(m, inndata, clauses,Shape_X, Shape_Y, Shape_Z, Window_X, Window_Y,machine, Name, dim, timestr)
    results = open("Results/" + Name + "/" + machine + "/" + machine + dim + timestr + ".csv", 'a')
    results.write("mean,")
    meancount=0
    meansepoch = 0
    highepoch = 0
    for i in meanTab:
        meancount+=1
        meansepoch += i/kFold
        if i/kFold > highepoch:
            highepoch = i/kFold
        results.write(",%.4f" % (i/kFold))
    results.write("\n")
    results.write("Single/k-Fold/Average")
    results.write(",%.4f" % (Highest))
    results.write(",%.4f" % (highepoch)) # should be highest epoch
    results.write(",%.4f" % (meansepoch / meancount))
    print("Highest: %.4f Highest k-Fold: %.4f Average k-Fold: %.4f" % (Highest, highepoch, meansepoch/meancount))
    results.close()

def runner():
    # Settings
    clauses = 32000
    Threshold = 10000
    S = 27.0
    epoch = 15
    #dim = "9x9Natsukaze_"
    dim = "9x9Aya_"
    #dim = "0.75_9x9Aya_"
    #dim = "0.5_9x9Aya_"
    kFold = 10
    machine = "TM"    #cTM or TM
    #inndata = "Natsukaze_NoDraw"
    inndata = "Draw"
    Window_X = 5
    Window_Y = 5
    Shape_X = 9
    Shape_Y = 9
    Shape_Z = 2
    Name = "Trond"
    Write_Clauses = 0  #0 = don't print clauses, 1-10 which k-Fold to write clauses for.
    savestate = 2  #0 = no save, #1 = save each kFold  #2 = save each epoch
    loadstate = 0
    #loadfile = "0211-1111"
    loadfile = "0210-2343"
    #StartMachine(clauses, epoch, Threshold, S, inndata,dim,machine,Window_X,Window_Y,Shape_X,Shape_Y,Shape_Z,Name, Write_Clauses,kFold)
    #StartMachine(8000, epoch, Threshold, S, inndata,dim,machine,Window_X,Window_Y,Shape_X,Shape_Y,Shape_Z,Name, Write_Clauses,kFold)
    StartMachine(clauses, epoch, Threshold, S, inndata,dim,machine,Window_X,Window_Y,Shape_X,Shape_Y,Shape_Z,Name, Write_Clauses,kFold, savestate, loadstate, loadfile)


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
