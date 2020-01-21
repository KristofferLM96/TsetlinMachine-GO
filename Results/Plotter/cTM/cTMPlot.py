from matplotlib import pyplot
from statistics import stdev ,median
import os
import glob
path = ''
XLABEL = "epochs"
YLABEL = "accuracy"
OFFSET = 0
CI = True

kFold = 1  # 1 or 10
showT1 = [0,8,12,19] #specify which epochs will go out. epoch 0 will show as epoch 1 in table.
OutputFileName = "TM9x9Natsukaze" #outputname for each file
Caption = "Testing 9x9 dataset with TM under different settings."  #table caption
label ="tab:"+OutputFileName #table label
parsing = "Settings"
backslash = "\ "
backslash = backslash[:1]
table = open(OutputFileName+".txt",'w')
table.write(backslash + "FloatBarrier\n")
table.write(backslash + "begin{table}[h!]\n")
table.write(backslash + "centering\n")
table.write(backslash + "begin{tabular}{|a|d|d|d|d|d|}\n")
table.write(backslash + "hline\n")
table.write(backslash + "rowcolor{Blue}\n")
table.write(backslash + "begin{tabular}[c]{@{}l@{}}"+ parsing+backslash+"end{tabular}&")
table.write(backslash + "begin{tabular}[c]{@{}l@{}} Epoch "+str(showT1[0]+1)+backslash+"end{tabular}&")
table.write(backslash + "begin{tabular}[c]{@{}l@{}} Epoch "+str(showT1[1]+1)+backslash+"end{tabular}&")
table.write(backslash + "begin{tabular}[c]{@{}l@{}} Epoch "+ str(showT1[2]+1)+backslash+"end{tabular}&")
#table.write(backslash + "begin{tabular}[c]{@{}l@{}} Epoch "+ str(showT1[3]+1)+backslash+"end{tabular}&")
table.write(backslash + "begin{tabular}[c]{@{}l@{}} Epoch "+ str(showT1[3]+1)+backslash+"end{tabular}"+backslash+backslash+" "+backslash+"hline\n")
for FILENAME in glob.glob(os.path.join(path, '*.csv')):
    #print(FILENAME)
    m = []
    s = []
    c = 0
    counter =0
    tab = []
    names = ""
    average = 0
    with open(f"{FILENAME}", 'r') as file:
        #print(FILENAME)
        lined=[]
        setting = ""
        machine = ""
        for line in file.readlines():
            counter+=1
            if counter == 1:
                lineds = [str(x) for x in line.strip().split(',')]
                linesd = str(lineds[0])
                if lineds[-2][0] == "A":
                    average = 1
                machine = linesd[10]
            if counter == 3:
                lineds = [str(x) for x in line.strip().split(',')]
                linesd =  str(lineds[1])
                linede = linesd[:-2]
                names = names+linede +"c "
                setting = setting + linede + "/"
            if counter == 4:
                lineds = [str(x) for x in line.strip().split(',')]
                linesd = str(lineds[1])
                linede = linesd[:-2]
                names = names+linede +"t "
                setting = setting + linede + "/"
            if counter == 5:
                lineds = [str(x) for x in line.strip().split(',')]
                linesd = str(lineds[1])
                linede = linesd[:-2]
                names = names+linede +"s "
                setting = setting + linede + "/"
            if machine == "C":
                if counter == 6:
                    lineds = [str(x) for x in line.strip().split(',')]
                    linesd = str(lineds[1])
                    linede = linesd[:-2]
                    names = names+linede +"x"+linede+"w "
                    setting = setting + linede+"x"+linede
                if counter == 11:
                    lineds = [str(x) for x in line.strip().split(',')[:1]]
                    names = names + str(lineds[0])
                    names = names[:-6]
                if counter > 10 and counter < 21:
                    line = [float(x) for x in line.strip().split(',')[2:]]
                    if average == 1:
                        line = line[0:-1]
                    tab.append(line)

            elif machine == "T":
                if counter == 6:
                    lineds = [str(x) for x in line.strip().split(',')[:1]]
                    names = names + str(lineds[0])
                    names = names[:-6]
                if counter > 5 and counter < 16:
                    line = [float(x) for x in line.strip().split(',')[2:]]
                    if average ==1:
                        line = line[0:-1]
                    tab.append(line)
        if kFold == 10:
            for i in range(len(line)):
                m.append(median([tab[0][i],tab[1][i],tab[2][i],tab[3][i],tab[4][i],tab[5][i],tab[6][i],tab[7][i],tab[8][i],tab[9][i]]))
                s.append(stdev([tab[0][i],tab[1][i],tab[2][i],tab[3][i],tab[4][i],tab[5][i],tab[6][i],tab[7][i],tab[8][i],tab[9][i]]))
        else:
            for i in range(len(line)):
                m.append(tab[0][i])
                s.append(tab[0][i])
        #print(names)
        backslash = "\ "
        backslash = backslash[:1]
        table.write(backslash+"begin{tabular}[c]{@{}l@{}} "+setting+"\end{tabular}\n")
        table.write("&"+backslash+"begin{tabular}[c]{@{}l@{}}"+str(round(m[showT1[0]],2))+backslash+"%$"+backslash+"pm"+str(round(s[showT1[0]],2))+backslash+"%$"+backslash+"end{tabular}\n")
        table.write("&"+backslash+"begin{tabular}[c]{@{}l@{}}"+str(round(m[showT1[1]],2))+backslash+"%$"+backslash+"pm"+str(round(s[showT1[1]],2))+backslash+"%$"+backslash+"end{tabular}\n")
        table.write("&"+backslash+"begin{tabular}[c]{@{}l@{}}"+str(round(m[showT1[2]],2))+backslash+"%$"+backslash+"pm"+str(round(s[showT1[2]],2))+backslash+"%$"+backslash+"end{tabular}\n")
        #table.write("&"+backslash+"begin{tabular}[c]{@{}l@{}}" + str(round(m[showT1[3]], 2)) + backslash + "%$" + backslash + "pm" + str(round(s[showT1[3]], 2)) + backslash + "%$" + backslash + "end{tabular}\n")
        table.write("&"+backslash+"begin{tabular}[c]{@{}l@{}}"+str(round(m[showT1[3]],2))+backslash+"%$"+backslash+"pm"+str(round(s[showT1[3]],2))+backslash+"%$"+backslash+"end{tabular}"+backslash+backslash+" "+backslash+"hline\n")



    x = [i+1 for i in range(len(m))]
    if kFold == 10:
        if CI:
            CI_low = [(m[i]-2*s[i]) for i in x]
            CI_high =[(m[i]+2*s[i]) for i in x]
            pyplot.fill_between(x, CI_low, CI_high, alpha=0.4)
    pyplot.plot(x, m, lw=1, label=f"{names}")
    #x = [(i+OFFSET) for i in x]
table.write(backslash + "end{tabular}\n")
table.write(backslash + "caption{" +Caption + "}\n")
table.write(backslash + "label{" + label + "}\n")
table.write(backslash + "end{table}\n")
table.write(backslash + "FloatBarrier\n")
pyplot.legend(loc='best')
TITLE = ""
pyplot.title(TITLE)
pyplot.xlabel(XLABEL)
pyplot.ylabel(YLABEL)
pyplot.savefig(OutputFileName, dpi=300)
pyplot.show()
