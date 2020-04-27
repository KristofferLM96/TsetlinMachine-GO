import math
import csv
TMopen0 = open("TM90_100T_9x9Aya_0310-1342-clauses0.csv",'r')
TMopen1 = open("TM90_100T_9x9Aya_0310-1342-clauses1.csv",'r')
TMopen2 = open("TM90_100T_9x9Aya_0310-1342-clauses2.csv",'r')
TMr0 = TMopen0.readlines()
TMr1 = TMopen1.readlines()
TMr2 = TMopen2.readlines()

#rows = "0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1"
def returnValue(t1,t2):
    if (t1 == "1"):
        return "X"
    elif (t2 == "1"):
        return "O"
    elif (t1 == ","):
        return " "
    else:
        return "#"
#print(rows[:83])
#print(rows[84:167])
#b,b,b,b,b,b,b,b,b,b,b,b,x,o,b,b,b,b,x,o,x,o,x,o,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,win
#i = 0
#newline = rows[:83]
#newline2 = rows[84:167]
#print(newline)
#print(newline2)
def makeBoard2(input, rows, columns):
    input = input[:-1]
    input = input.split(",")
    outcome = input[-1]
    inputx = input[:81]
    inputo = input[81:162]
    #print(input)
    #print(inputx)
    #print(inputo)
    i=0
    for column in range(columns):
        outline = ""
        for row in range(rows):
            output = ""
            if(inputx[i] == inputo[i]):
                output = "_"
            elif(inputx[i] == "1"):
                output = "X"
            elif(inputo[i] == "1"):
                output = "O"
            outline = outline + ","+output
            i=i+1
        print(outline)
    #print(outcome)
#for i in range(0,5,1):
#    makeBoard2(win[i],7,6)
    #print("---------------------")
#print("--------------------------")
#for i in range(9998,10003,1):
#    makeBoard2(win[i],7,6)
    #print("---------------------")
#print("--------------------------")
#for i in range(24000,24005,1):
#    makeBoard2(win[i],7,6)
    #print("---------------------")
def makeBoard(input, rows, columns):
    mellomrom = " "
    one = " "
    uLine = "  "
    underline = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
    input = input[:-1]
    input = input.split(",")
    #print(input)
    i=0
    for column in range(columns):
        outline = str(rows-column)
        for row in range(rows):
            outline = outline + mellomrom+transform(input[i])
            i=i+1
        print(outline)
    for i in range(rows):
        uLine +=one+underline[i] + mellomrom
    print(uLine)
def transform(input):
    # print(input)
    if (int(input[0])==1 and int(input[2])==1) or (int(input[1])==1 and int(input[3])==1):
        return "Fa"
    elif (int(input[0])==1 and int(input[1])==1):
        return "+#"
    elif (int(input[2])==1 and int(input[3])==1):
        return "-#"
    elif int(input[0])==1:
        return "+B"
    elif int(input[1])==1:
        return "+W"
    elif int(input[2])==1:
        return "-b"
    elif int(input[3])==1:
        return "-w"
    else:
        return "  "
        #return "?#"
def prints(status,clause, posneg,truefalse):
    if status == "Win":
        board = TMr1[clause]
    else:
        board = TMr0[clause]
    print("%s Clause %s %s %s"%(status,clause,truefalse,posneg))
    makeBoard(board, 9, 9)
prints("Loss",250,"Positive", "True")
#prints("Loss",880,"Positive", "True")
prints("Loss",468,"Positive","False")
prints("Win",208,"Positive", "True")
prints("Win",856,"Positive","False")

prints("Loss",591,"Negative", "True")
#prints("Loss",39,"Negative", "True")
prints("Loss",377,"Negative","False")
#prints("Loss",99,"Negative","False")
prints("Win",905,"Negative", "True")
#prints("Win",235,"Negative", "True")
prints("Win",503,"Negative","False")
#prints("Win",95,"Negative","False")



