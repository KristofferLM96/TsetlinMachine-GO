import os
import glob
import time
import gomill.boards

path = 'Data/20181218natsukaze_self'
output_path = "Data/Binary/9x9Natsukaze_binary.txt"
board_size = 9
total_pos = 19
time_start = time.time()
timestr = time.strftime("%Y-%m/%d--%H-%M-%S")
print("Stating at " + timestr, "\n")


def init_board():
    global end_board
    mainTab = []
    for i in range(board_size):
        tempTab = []
        for i in range(board_size):
            tempTab.append("+")
        mainTab.append(tempTab)
    return mainTab


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


def load_board(in_board, out_board):
    result = in_board[0].split("RE")
    results = 2
    if result[1][1] == "W":
        results = 0
    if result[1][1] == "B":
        results = 1
    _move_list = []
    for row in in_board[1:-1]:
        x = translate(row[3])
        y = translate(row[4])
        res = row[1]
        if row[1] == "B":
            move = ["b", x, y]
        if row[1] == "W":
            move = ["w", x, y]
        if x != total_pos and y != total_pos:
            out_board[x][y] = res
            _move_list.append(move)
    return out_board, results, _move_list


def play(_turn):
    global game_board
    x = _turn[1]
    y = _turn[2]
    color = _turn[0]
    game_board.play(x, y, color)


def get_board():
    global end_board
    global game_board
    for y in range(board_size):
        for x in range(board_size):
            pos = game_board.get(x, y)
            if pos == "w" or pos == "b":
                end_board.append(pos)
            else:
                end_board.append("+")


def print_board():
    global end_board
    pos = 0
    for i in range(board_size):
        print_string = ""
        for j in range(board_size):
            print_string = print_string + " " + end_board[pos]
            pos = pos + 1
        print(print_string)


def convert():
    global end_board
    w_bit = ''
    b_bit = ''
    for index in range(len(end_board)):
        if end_board[index] == "w":
            w_bit = w_bit + '1,'
            b_bit = b_bit + '0,'
        elif end_board[index] == "b":
            b_bit = b_bit + '1,'
            w_bit = w_bit + '0,'
        else:
            w_bit = w_bit + '0,'
            b_bit = b_bit + '0,'

    return b_bit + w_bit


def write_file(_output):
    global binary_board
    _output.write(binary_board + "\n")


def main(input, _board):
    global binary_board
    boards, result, move_list = load_board(input, _board)
    # print("Moves:",  move_list)

    for turn in move_list:
        play(turn)

    get_board()
    # print_board()
    binary_board = convert()
    binary_board = binary_board + str(result)


counter = 1
output = open(output_path, 'w+')
total_files = len(glob.glob(os.path.join(path+"/*", '*.sgf')))
for infile in glob.glob(os.path.join(path+"/*", '*.sgf')):
    start_time = time.time()
    end_board = []
    game_board = gomill.boards.Board(board_size)
    binary_board = ""
    file = open(infile, 'r')
    lines = file.readlines()
    main(lines, init_board())
    write_file(output)
    counter = counter + 1
    print("Converting file", counter, "out of", total_files, "files. .................. ",
          round((counter / total_files * 100), 2), "% ..................",
          round((time.time() - start_time) * 1000, 2), "ms")
    file.close()
output.close()
timestr = time.strftime("%Y-%m/%d--%H-%M-%S")
print("Stopping at " + timestr, "\n")
print("It took ", (time.time() - time_start) / 60, "minutes")
