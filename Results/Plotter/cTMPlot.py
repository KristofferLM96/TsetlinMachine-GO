from matplotlib import pyplot
from statistics import stdev, mean
import os
import glob
path = 'input/'
XLABEL = "epochs"
YLABEL = "accuracy"
OFFSET = 0
CI = True

kFold = 10  # 1 or 10
#showT1 = [0, 4, 8, 12,14]  # specify which epochs will go out. epoch 0 will show as epoch 1 in table.
showT1 = [0, 4, 9, 14] # showing 4 epochs + average of last 10 epochs.
OutputFileName = "cTM9x9Aya32k8k40sDim"  # outputname for each file
# table caption ..
Caption = "Testing 9x9 dataset using cTM with 32000 clauses, 8000 thresholds, 40s under different window sizes."
label = OutputFileName  # table label
parsing = "Window"  # Threshold, Window, Settings, Clauses, S
epoch = 15
standdev = 0  # 1 if enabled in graph, 0 if not
title_graph = ""
backslash = "\ "
backslash = backslash[:1]
table = open("output/" + OutputFileName + ".txt", 'w')

table.write(backslash + "FloatBarrier\n")
table.write(backslash + "begin{figure}[h!]\n")
table.write("    " + backslash + "centering\n")
table.write("    " + backslash + "includegraphics[scale=.6]{Images/Results/" + OutputFileName + ".png}\n")
table.write("    " + backslash + "caption{" + Caption + "}\n")
table.write("    " + backslash + "label{fig:" + label + "}\n")
table.write(backslash + "end{figure}\n")
table.write(backslash + "FloatBarrier\n")
table.write(backslash + "FloatBarrier\n")
table.write(backslash + "begin{table}[h!]\n")
table.write(backslash + "centering\n")
if len(showT1) == 5:
    table.write(backslash + "begin{tabular}{|a|d|d|d|d|d|}\n")
if len(showT1) == 4:
    table.write(backslash + "begin{tabular}{|a|d|d|d|d||x|}\n")
table.write(backslash + "hline\n")
table.write(backslash + "rowcolor{Blue}\n")
table.write(backslash + "begin{tabular}[c]{@{}l@{}}" + parsing+backslash + "end{tabular}&")
table.write(backslash + "begin{tabular}[c]{@{}l@{}} Epoch " + str(showT1[0] + 1) + backslash + "end{tabular}&")
table.write(backslash + "begin{tabular}[c]{@{}l@{}} Epoch " + str(showT1[1] + 1) + backslash + "end{tabular}&")
table.write(backslash + "begin{tabular}[c]{@{}l@{}} Epoch " + str(showT1[2] + 1) + backslash + "end{tabular}&")
table.write(backslash + "begin{tabular}[c]{@{}l@{}} Epoch " + str(showT1[3] + 1) + backslash + "end{tabular}")
ttitle = ""
ctitle = ""
wtitle = ""
stitle = ""
if len(showT1) == 5:
    table.write("&")
    table.write(backslash + "begin{tabular}[c]{@{}l@{}} Epoch " + str(showT1[4] + 1) + backslash + "end{tabular}")
if len(showT1) == 4:
    table.write("&")
    table.write(backslash + "begin{tabular}[c]{@{}l@{}} Last 10 Epoch"+ backslash + "end{tabular}")
table.write(backslash + backslash + " " + backslash + "hline\n")
for FILENAME in sorted(glob.glob(os.path.join(path, '*.csv'))):
    print(FILENAME)
    m = []
    s = []
    c = 0
    counter = 0
    tab = []
    names = ""
    namestab = []
    average = 0
    with open(f"{FILENAME}", 'r') as file:
        #print(FILENAME)
        lined = []
        setting = ""
        threshold = ""
        window = ""
        clauses = ""
        machine = ""
        sparam = ""
        for line in file.readlines():
            counter += 1
            if counter == 1:
                lineds = [str(x) for x in line.strip().split(',')]
                linesd = str(lineds[0])
                if lineds[-2][0] == "A":
                    average = 1
                machine = linesd[10]
            if counter == 3:
                lineds = [str(x) for x in line.strip().split(',')]
                linesd = str(lineds[1])
                linede = linesd[:-2]
                clauses = linede
                namestab.append(clauses)
                names = names + linede + "c "
                setting = setting + linede + "/"
            if counter == 4:
                lineds = [str(x) for x in line.strip().split(',')]
                linesd = str(lineds[1])
                linede = linesd[:-2]
                threshold = linede
                namestab.append(threshold)
                names = names + linede + "t "
                setting = setting + linede + "/"
            if counter == 5:
                lineds = [str(x) for x in line.strip().split(',')]
                linesd = str(lineds[1])
                linede = linesd[:-2]
                namestab.append(linede)
                sparam= linesd
                names = names + linede + "s "
                setting = setting + linede + "/"
            if machine == "C":
                if counter == 6:
                    lineds = [str(x) for x in line.strip().split(',')]
                    linesd = str(lineds[1])
                    linede = linesd[:-2]
                    window = linede + "x" + linede
                    namestab.append(window)
                    names = names + linede + "x" + linede + "w "
                    setting = setting + linede + "x" + linede
                if counter == 11:
                    lineds = [str(x) for x in line.strip().split(',')[:1]]
                    names = names + str(lineds[0])
                    names = names[:-6]
                    temp = str(lineds[0])
                    temp = temp[:-6]
                    namestab.append(temp)
                if 21 > counter > 10:
                    line = [float(x) for x in line.strip().split(',')[2:]]
                    if average == 1:
                        line = line[0:-1]
                    tab.append(line)

            elif machine == "T":
                if counter == 6:
                    lineds = [str(x) for x in line.strip().split(',')[:1]]
                    names = names + str(lineds[0])
                    names = names[:-6]
                    temp = str(lineds[0])
                    temp = temp[:-6]
                    namestab.append(temp)
                if 16 > counter > 5:
                    line = [float(x) for x in line.strip().split(',')[2:]]
                    #print(counter)
                    #print(line)
                    if average == 1:
                        line = line[0:-1]
                    tab.append(line)
        if kFold == 10:
            for i in range(epoch):
                m.append(mean([tab[0][i], tab[1][i], tab[2][i], tab[3][i], tab[4][i], tab[5][i], tab[6][i], tab[7][i],
                                 tab[8][i], tab[9][i]]))
                s.append(stdev([tab[0][i], tab[1][i], tab[2][i], tab[3][i], tab[4][i], tab[5][i], tab[6][i], tab[7][i],
                                tab[8][i], tab[9][i]]))
        else:
            for i in range(len(tab)):
                m.append(tab[0][i])
                s.append(tab[0][i])
        #print(names)
        backslash = "\ "
        backslash = backslash[:1]
        labelinput = ""
        if parsing[0] == "T":
            labelinput = threshold
            names = threshold + " threshold"
            title_graph = namestab[-1] + ", " + clauses + " clauses, " + namestab[2] + " s"
        elif parsing[0] == "C":
            labelinput = clauses
            names = clauses + " clauses"
            title_graph = namestab[-1] + ", " + threshold + " threshold, " + namestab[2] + " s"
        elif parsing[0] == "W":
            labelinput = window
            title_graph = namestab[-1] + ", " + clauses + " clauses, " + threshold + " threshold, " + namestab[2] + " s"
            names = window + " window"
        elif parsing[0] == "S" or parsing[0] == "s":
            labelinput = sparam
            title_graph = namestab[-1] + ", " + clauses + " clauses, " + threshold + " threshold"
            names = sparam + " s"
        else:
            labelinput = setting
            title_graph = namestab[-1]

        table.write(backslash + "begin{tabular}[c]{@{}l@{}} " + labelinput + "\end{tabular}\n")
        table.write("&" + backslash + "begin{tabular}[c]{@{}l@{}}" + str(round(m[showT1[0]], 2)) + backslash + "%$" +
                    backslash + "pm"+str(round(s[showT1[0]], 2)) + backslash + "%$" + backslash + "end{tabular}\n")
        table.write("&" + backslash + "begin{tabular}[c]{@{}l@{}}" + str(round(m[showT1[1]], 2)) + backslash+"%$"
                    + backslash + "pm" + str(round(s[showT1[1]], 2)) + backslash+"%$" + backslash + "end{tabular}\n")
        table.write("&" + backslash + "begin{tabular}[c]{@{}l@{}}" + str(round(m[showT1[2]], 2)) + backslash+"%$"
                    + backslash + "pm" + str(round(s[showT1[2]], 2)) + backslash + "%$" + backslash + "end{tabular}\n")
        table.write("&" + backslash + "begin{tabular}[c]{@{}l@{}}" + str(round(m[showT1[3]], 2)) + backslash + "%$"
                    + backslash + "pm" + str(round(s[showT1[3]], 2)) + backslash + "%$" + backslash + "end{tabular}")
        if len(showT1) == 5:
            table.write("\n")
            table.write("&" + backslash + "begin{tabular}[c]{@{}l@{}}" + str(round(m[showT1[4]], 2)) + backslash+"%$"
                        + backslash + "pm" + str(round(s[showT1[4]], 2)) + backslash+"%$" + backslash + "end{tabular}")
        lastten = 0
        for i in m[-10:]:
            lastten += i
        lastten = lastten /10
        if len(showT1) == 4:
            table.write("\n")
            table.write("&" + backslash + "begin{tabular}[c]{@{}l@{}}" + str(round(lastten, 2)) + backslash + "%"
                        + backslash + "end{tabular}")
        table.write(backslash + backslash+" " + backslash + "hline\n")

    x = [i + 1 for i in range(len(m))]
    if kFold == 10 and standdev == 1:
        if CI:
            CI_low = [(m[i - 1] - 2 * s[i - 1]) for i in x]
            CI_high = [(m[i - 1] + 2 * s[i - 1]) for i in x]
            pyplot.fill_between(x, CI_low, CI_high, alpha=0.4)
    pyplot.plot(x, m, lw=2, label=f"{names}")

    #x = [(i+OFFSET) for i in x]
table.write(backslash + "end{tabular}\n")
table.write(backslash + "caption{" + Caption + "}\n")
table.write(backslash + "label{tab:" + label + "}\n")
table.write(backslash + "end{table}\n")
table.write(backslash + "FloatBarrier\n")
pyplot.legend(loc='best')
TITLE = title_graph
pyplot.gca().set_xlim([1, epoch])
pyplot.xticks(x)
pyplot.title(TITLE)
pyplot.xlabel(XLABEL)
pyplot.ylabel(YLABEL)
pyplot.grid(zorder=0)
pyplot.savefig("output/" + OutputFileName, dpi=300)
pyplot.show()
