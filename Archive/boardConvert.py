import os
import glob
import Go
import time


timestr = time.strftime("%Y%-m%/d--%H-%M-%S")
print("Stating at "+timestr)
path = 'Data/20181218natsukaze_self/01'
output = open("9x9binary.txt", 'w+')

board_size = 9
total_pos = 19


def board(inboard):
    result = inboard[0].split("RE")
    results = 2
    if result[1][1] == "W":
        results = 0
    if result[1][1] == "B":
        results = 1
    table = []
    for row in inboard[1:-1]:
        x = translate(row[3])
        y = translate(row[4])
        move = [row[1], x, y]

        # print(x,y,res)
        if x != total_pos and y != total_pos:
            table.append(move)
    return results, table


def translate(i):
    if i == "a":
        return 0
    if i == "b":
        return 1
    if i == "c":
        return 2
    if i == "d":
        return 3
    if i == "e":
        return 4
    if i == "f":
        return 5
    if i == "g":
        return 6
    if i == "h":
        return 7
    if i == "i":
        return 8
    if i == "j":
        return 9
    if i == "k":
        return 10
    if i == "l":
        return 11
    if i == "m":
        return 12
    if i == "n":
        return 13
    if i == "o":
        return 14
    if i == "p":
        return 15
    if i == "q":
        return 16
    if i == "r":
        return 17
    if i == "s":
        return 18
    if i == "t":
        return 19


def convert(input):
    i = 0
    w_bit = ''
    b_bit = ''
    rows = ''
    for i in range(len(input)):
        for j in range(len(input)):
            if input[i][j] == 'x':
                w_bit = w_bit + '1,'
                b_bit = b_bit + '0,'
            elif input[i][j] == 'o':
                b_bit = b_bit + '1,'
                w_bit = w_bit + '0,'
            else:
                w_bit = w_bit + '0,'
                b_bit = b_bit + '0,'
    return b_bit + w_bit


for infile in glob.glob(os.path.join(path, '*.sgf')):
    # print("current file is: " + infile)
    file = open(infile, 'r')
    lines = file.readlines()
    result, nTab = board(lines)
    game = Go.Binput(board_size, nTab)
    # print(game)
    wb_bit = convert(game)
    wb_bit = wb_bit + str(result)
    output.write(wb_bit + "\n")
output.close()
timestr = time.strftime("%Y%m%d-%H%M%S")
print("Stopping at " + timestr)
