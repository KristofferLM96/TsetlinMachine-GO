import os
import glob
import time
import gomill.boards
import gomill.ascii_boards

board_print = False
full_board = False
current_results = False
moves_count = True
threshold = True
move_count = 80
move_threshold = 90

print("Settings:")
print("--------------------------------------------")
print("board_print:", board_print)
print("full_board:", full_board)
print("current_results:", current_results)
print("moves_count:", moves_count)
print("move_count:", move_count)
print("move_threshold:", move_threshold)

x_axis = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
          "K", "L", "M", "N", "O", "P", "Q", "R", "S"]
if not moves_count:
    if not full_board:
        completion_percentage = 0.5
    else:
        completion_percentage = 1
    print("completion_percentage:", completion_percentage)

komi = 7
name = "9x9Aya"
# path = "Data/Original/" + name + "/*"
path = "/home/kristoffer/Documents/Data/Original/9x9_10k_r104_144x20k/*"

if full_board:
    output_path = "Data/Binary/" + name + "_binary.txt"
elif not full_board and not moves_count:
    if current_results:
        output_path = "Data/Binary/" + str(completion_percentage) + "_1_" + name + "_binary.txt"
    else:
        output_path = "Data/Binary/" + str(completion_percentage) + "_" + name + "_binary.txt"
else:
    if threshold:
        output_path = "Data/Binary/" + str(move_count) + "_" + str(move_threshold) + "T" + "_" + name + "_binary.txt"
    else:
        output_path = "Data/Binary/" + str(move_count) + "_" + name + "_binary.txt"

board_size = 9
total_pos = 19
time_start = time.time()
timestr = time.strftime("%Y-%m/%d--%H-%M-%S")

print("komi:", komi)
print("path:", path)
print("output_path:", output_path)
print("--------------------------------------------", "\n")

print("Starting at " + timestr, "\n")


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


def load_game(_game_lines, _board_state):
    result = _game_lines[0].split("RE")
    if "HA[" in _game_lines[0]:
        handicap = int(_game_lines[0].split("HA[")[1][0])
    else:
        handicap = 0
    results = 2
    if result[1][1] == "W":
        results = 0
    if result[1][1] == "B":
        results = 1
    _move_list = []
    const = 4
    for row in _game_lines[1:-1]:
        x = translate(row[3])
        y = translate(row[4])
        res = row[1]
        if row[1] + row[2] == "AB":
            res = row[2]
            for i in range(handicap):
                x = translate(row[4 + (i * const)])
                y = translate(row[5 + (i * const)])
                _move = ["b", x, y]
                if x != total_pos and y != total_pos:
                    _board_state[x][y] = res
                    _move_list.append(_move)
        else:
            if row[1] == "B":
                _move = ["b", x, y]
            if row[1] == "W":
                _move = ["w", x, y]
            if x != total_pos and y != total_pos:
                _board_state[x][y] = res
                _move_list.append(_move)
    return _board_state, results, _move_list


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
                end_board.append("·")


def print_board():
    global end_board
    global x_axis
    y_axis = board_size
    pos = 0
    for i in range(board_size):
        print_string = str(y_axis)
        for j in range(board_size):
            print_string = print_string + "  " + end_board[pos]
            pos = pos + 1
        y_axis -= 1
        print(print_string)
    axis_str = " "
    for axis in range(board_size):
        axis_str = axis_str + "  " + x_axis[axis]
    print(axis_str)


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


def main(_file_lines, _board):
    global errors
    global binary_board
    global game_board
    boards, result, move_list = load_game(_file_lines, _board)
    count = 0
    if moves_count:
        move_range = move_count
    else:
        move_range = int(len(move_list) * completion_percentage)
    if len(move_list) < move_count:
        print("Skipping game.. not enough moves.")
        return -1
    if threshold:
        if len(move_list) < move_threshold:
            print("Skipping game.. below move threshold.")
            return -1
    for turn in move_list[:move_range]:
        count += 1
        try:
            play(turn)
        except ValueError:
            errors += 1
            print("Something went wrong. Could not convert file.", infile)
            break

    get_board()
    area_score = game_board.area_score() - komi
    if board_print:
        print("Total turns:", len(move_list))
        print("Turns done:", count)
        print("Area Score:", area_score, "\n")
        print("   | Board End Positions |")
        print("-----------------------------")
        print_board()
        print("-----------------------------")
        print("\n")
    binary_board = convert()
    if not current_results:
        binary_board = binary_board + str(result)
    else:
        if area_score < 0:
            binary_board = binary_board + "0"
        elif area_score == 0:
            binary_board = binary_board + "2"
        else:
            binary_board = binary_board + "1"

    return 1


errors = 0
counter = 1
output = open(output_path, 'w+')
total_files = len(glob.glob(os.path.join(path, '*.sgf')))
for infile in glob.glob(os.path.join(path, '*.sgf')):
    start_time = time.time()
    end_board = []
    game_board = gomill.boards.Board(board_size)
    binary_board = ""
    file = open(infile, 'r', encoding="ISO-8859-1")
    file_lines = file.readlines()
    print(infile)
    print("Converting file", counter, "out of", total_files, "files. ............................................... ",
          round((counter / total_files * 100), 2), "% ............................................... ",
          round((time.time() - start_time) * 1000, 2), "ms")
    write_check = main(file_lines, init_board())
    print("\n")
    if not write_check == -1:
        write_file(output)
    counter = counter + 1
    file.close()
output.close()
timestr = time.strftime("%Y-%m/%d--%H-%M-%S")
print("Stopping at " + timestr, "\n")
print("It took ", round((time.time() - time_start) / 60, 2), "minutes")
print("\n" + "Errors:", errors)
