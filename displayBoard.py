import GoC as GoGame
go1 = open("20180704_2258_00001.sgf",'r')
go2 = open("20180704_2318_00005.sgf",'r')
go3 = open("20180704_2332_00005.sgf",'r')
go4 = open("01/20180709_0621_00934.sgf",'r')
go1r = go1.readlines()
go2r = go2.readlines()
go3r = go3.readlines()
go4r = go4.readlines()

def newBoard():
    mainTab = []
    for i in range(9):
        tempTab = []
        for i in range(9):
            tempTab.append("+")
        mainTab.append(tempTab)
    return mainTab

def translate(i):
    if i == "a": return 0
    if i == "b": return 1
    if i == "c": return 2
    if i == "d": return 3
    if i == "e": return 4
    if i == "f": return 5
    if i == "g": return 6
    if i == "h": return 7
    if i == "i": return 8
    if i == "j": return 9
    if i == "k": return 10
    if i == "l": return 11
    if i == "m": return 12
    if i == "n": return 13
    if i == "o": return 14
    if i == "p": return 15
    if i == "q": return 16
    if i == "r": return 17
    if i == "s": return 18
    if i == "t": return 19
def board(inboard,outboard):
    result = inboard[0].split("RE")
    #size = inboard[0].split("SZ")
    #bsize = size[1].split("]")
    results ="draw"
    if result[1][1] == "W": results = "loss"
    if result[1][1] == "B": results = "win"
    #print(result[1])
    table=[]
    for row in inboard[1:-1]:
        #move =[]
        x = translate(row[3])
        y = translate(row[4])
        res = row[1]
        move =[row[1],x,y]

        #print(x,y,res)
        if x != 19 and y != 19:
            outboard[x][y] = res
            table.append(move)
    return outboard,results, table

#print(mainTab)
def printBoard(input,board1):#board,result):
    boards,result, nTab =board(input,board1)
    print("Black "+result)
    for i in range(9):
        tempPrint =""
        for j in range(9):
            tempPrint = tempPrint+boards[j][i]
        print (tempPrint)
    print (nTab)
    game =GoGame.Binput(9,nTab)

printBoard(go1r,newBoard())
print("---")
printBoard(go2r,newBoard())
print("---")
printBoard(go3r,newBoard())
print("---")
printBoard(go4r,newBoard())