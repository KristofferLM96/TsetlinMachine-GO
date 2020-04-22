from matplotlib import pyplot
from statistics import stdev, mean
import os
import glob
path = 'input/'
XLABEL = "moves"
YLABEL = "accuracy"
OFFSET = 0
CI = True
showT1 = [0, 1, 3, 5,7] # showing 4 epochs + average of last 10 epochs.
# table caption ..
Caption = ""
label = "OutputFileName"  # table label
parsing = "Outcome"  # Threshold, Window, Settings, Clauses, S
epoch = 8
standdev = 0  # 1 if enabled in graph, 0 if not
title_graph = ""
backslash = "\ "
backslash = backslash[:1]

for FILENAME in sorted(glob.glob(os.path.join(path, '*.csv'))):
    print(FILENAME)

    with open(f"{FILENAME}", 'r') as file:
        m = []
        s = []
        m2 = []
        s2 = []
        perc1 = []
        perc2 = []
        c = 0
        counter = 0
        tab = []
        tab2 = []
        labelinput = "Correct white"
        labelinput2 = "Correct black"
        names = "White"
        names2 = "Black"
        namestab = []
        average = 0
        #print(FILENAME)
        lined = []
        Black = 0
        White = 0
        Total = 0
        for line in file.readlines():
            print(line)
            counter += 1
            if counter == 1:
                lineds = [str(x) for x in line.strip().split(',')]
                Caption = str(lineds[0])
            if counter == 2:
                lined = [int(x) for x in line.strip().split(',')]
                tab.append(lined)
                for i in range(len(tab)):
                    m.append(tab[i])
                    s.append(tab[i])
            if counter == 3:
                lined = [int(x) for x in line.strip().split(',')]
                tab2.append(lined)
                for i in range(len(tab2)):
                    m2.append(tab2[i])
                    s2.append(tab2[i])
        m = m[0]
        m2 = m2[0]
        s = s[0]
        s2 = s2[0]
        if counter == 4:
            lined = [str(x) for x in line.strip().split(',')]
            Black = lined[3]
            White = lined[1]
            Total = lined[5]
            for i in range(epoch):
                perc1.append(int(m[i])/int(White)*100)
                perc2.append(int(m2[i]) / int(Black) * 100)

        print(perc1)
        print(perc2)
        table = open("output/" + FILENAME[6:-4] + ".txt", 'w')
        table.write(backslash + "FloatBarrier\n")
        table.write(backslash + "begin{figure}[h!]\n")
        table.write("    " + backslash + "centering\n")
        table.write("    " + backslash + "includegraphics[scale=.6]{Images/Results/" + FILENAME[6:-4] + ".png}\n")
        table.write("    " + backslash + "caption{" + Caption + "}\n")
        table.write("    " + backslash + "label{fig:" + FILENAME[6:-4] + "}\n")
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
        if counter == 4:
            table.write(backslash + "begin{tabular}[c]{@{}l@{}}" + parsing + backslash + "end{tabular}&")
            table.write(backslash + "begin{tabular}[c]{@{}l@{}} B Move " + str(showT1[0]) + backslash + "end{tabular}&")
            table.write(backslash + "begin{tabular}[c]{@{}l@{}} B Move " + str(showT1[1]) + backslash + "end{tabular}&")
            table.write(backslash + "begin{tabular}[c]{@{}l@{}} B Move " + str(showT1[2]) + backslash + "end{tabular}&")
            table.write(backslash + "begin{tabular}[c]{@{}l@{}} B Move " + str(showT1[3]) + backslash + "end{tabular}")
            ttitle = ""
            ctitle = ""
            wtitle = ""
            stitle = ""
            if len(showT1) == 5:
                table.write("&")
                table.write(
                    backslash + "begin{tabular}[c]{@{}l@{}} B Move " + str(showT1[4]) + backslash + "end{tabular}")
            if len(showT1) == 4:
                table.write("&")
                table.write(backslash + "begin{tabular}[c]{@{}l@{}} Last 10 Epoch" + backslash + "end{tabular}")
            table.write(backslash + backslash + " " + backslash + "hline\n")

            #print(names)
            backslash = "\ "
            backslash = backslash[:1]
            table.write(backslash + "begin{tabular}[c]{@{}l@{}} " + labelinput2 + "\end{tabular}\n")
            table.write("&" + backslash + "begin{tabular}[c]{@{}l@{}}" + str(round(m2[showT1[0]], 2)) + backslash + "end{tabular}\n")
            table.write("&" + backslash + "begin{tabular}[c]{@{}l@{}}" + str(round(m2[showT1[1]], 2)) + backslash+ "end{tabular}\n")
            table.write("&" + backslash + "begin{tabular}[c]{@{}l@{}}" + str(round(m2[showT1[2]], 2)) + backslash + "end{tabular}\n")
            table.write("&" + backslash + "begin{tabular}[c]{@{}l@{}}" + str(round(m2[showT1[3]], 2)) + backslash + "end{tabular}")
            table.write("\n")
            table.write("&" + backslash + "begin{tabular}[c]{@{}l@{}}" + str(round(m2[showT1[4]], 2))+ backslash + "end{tabular}")
            table.write(backslash + backslash+" " + backslash + "hline\n")
            table.write(backslash + "begin{tabular}[c]{@{}l@{}} " + labelinput + "\end{tabular}\n")
            table.write("&" + backslash + "begin{tabular}[c]{@{}l@{}}" + str(round(m[showT1[0]], 2)) + backslash + "end{tabular}\n")
            table.write("&" + backslash + "begin{tabular}[c]{@{}l@{}}" + str(round(m[showT1[1]], 2)) + backslash+ "end{tabular}\n")
            table.write("&" + backslash + "begin{tabular}[c]{@{}l@{}}" + str(round(m[showT1[2]], 2)) + backslash + "end{tabular}\n")
            table.write("&" + backslash + "begin{tabular}[c]{@{}l@{}}" + str(round(m[showT1[3]], 2))+ backslash + "end{tabular}")
            table.write("\n")
            table.write("&" + backslash + "begin{tabular}[c]{@{}l@{}}" + str(round(m[showT1[4]], 2))+ backslash + "end{tabular}")
            table.write(backslash + backslash+" " + backslash + "hline\n")


    x2 = [i for i in range(len(perc2))]
    x = [i for i in range(len(perc1))]
    pyplot.plot(x2, perc2, lw=2, label=f"{names2}")
    pyplot.plot(x, perc1, lw=2, label=f"{names}")
    table.write(backslash + "end{tabular}\n")
    table.write(backslash + "caption{" + Caption + "}\n")
    table.write(backslash + "label{tab:" + FILENAME[6:-4] + "}\n")
    table.write(backslash + "end{table}\n")
    table.write(backslash + "FloatBarrier\n")
    pyplot.legend(loc='best')
    TITLE = title_graph
    pyplot.gca().set_xlim([1, epoch-1])
    pyplot.xticks(x)
    pyplot.title(Caption)
    pyplot.xlabel(XLABEL)
    pyplot.ylabel(YLABEL)
    pyplot.grid(zorder=0)
    pyplot.savefig("output/" + FILENAME[6:-4], dpi=300)
    pyplot.show()

    #x = [(i+OFFSET) for i in x]

