go1 = open("20180704_2258_00001.sgf",'r')
go2 = open("20180704_2318_00005.sgf",'r')
go3 = open("20180704_2332_00005.sgf",'r')
go1r = go1.readlines()
go2r = go2.readlines()
go3r = go3.readlines()

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
    if i == "t": return 9
def board(inboard,outboard):
    result = inboard.split
    for row in inboard[1:-1]:
        x = translate(row[3])
        y = translate(row[4])
        res = row[1]
        #print(x,y,res)
        if x != 9 and y != 9:
            outboard[x][y] = res
    return outboard

#print(mainTab)
def printBoard(board):
    for i in range(9):
        tempPrint =""
        for j in range(9):
            tempPrint = tempPrint+board[i][j]
        print (tempPrint)

printBoard(board(go1r,newBoard()))
print("---")
printBoard(board(go2r,newBoard()))
print("---")
printBoard(board(go3r,newBoard()))