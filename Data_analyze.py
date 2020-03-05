# -----------------------------------------------
# ................. LIBRARIES ...................
# -----------------------------------------------
import glob
import os
import time
import numpy as np


# -----------------------------------------------
# ............. GLOBAL VARIABLES ................
# -----------------------------------------------

name = "80_9x9Aya" # 9x9Natsukaze || 9x9Aya || x_9x9Aya .. x = amount moves
file_name = name + "_binary.txt"
binary_path = "Data/Binary/" + file_name
original_path = "/home/kristoffer/Documents/Data/Original/9x9_10k_r104_144x20k/*"
encoding = "UTF-8"  # ISO-8859-1 / UTF-8
multiple_files = True
unique_list = []
original_list = []
# [check_handicap(), check_duplication(), get_result_ratio(), check_moves(), remove_empty_lines()]
run_programs = [0, 1, 0, 0, 0]


# -----------------------------------------------
# ................. FUNCTIONS ...................
# -----------------------------------------------


def remove_empty_lines():
    output_file = open("Data/Binary/" + name + "_binary_1.txt", "w+")
    with open(binary_path, "r") as file:
        for line in file:
            if not line.isspace():
                output_file.write(line)


def check_handicap():
    file = open(original_path, 'r', encoding=encoding)
    file_lines = file.readlines()
    _handicap = file_lines[0].split("HA[")
    print(_handicap)
    handicap = _handicap[1][0]
    print(handicap)

    file.close()


def check_duplication():
    file = open(binary_path, 'r', encoding=encoding)
    global original_list
    global unique_list
    original_list = [line.strip() for line in file]
    print("Original List Length:", len(original_list))
    original_length = len(original_list)

    unique_list = np.unique(original_list)
    unique_length = len(unique_list)
    print("Unique List Length:", unique_length)
    print("Original - Unique:", original_length - unique_length, "\n")

    file.close()


def get_result_ratio():
    win = open("Data/Results-Split/" + name + "_win.txt", 'r')
    loss = open("Data/Results-Split/" + name + "_loss.txt", 'r')
    draw = open("Data/Results-Split/" + name + "_draw.txt", 'r')
    win_amount = len(win.readlines())
    loss_amount = len(loss.readlines())
    draw_amount = len(draw.readlines())
    total_amount = win_amount + loss_amount + draw_amount
    print("Amount of wins: ", win_amount, ",", round(((win_amount * 100) / total_amount)), "%")
    print("Amount of loss: ", loss_amount, ",", round(((loss_amount * 100) / total_amount)), "%")
    print("Amount of draw: ", draw_amount, ",", round(((draw_amount * 100) / total_amount)), "%")

    win.close()
    loss.close()
    draw.close()


def check_moves():
    total_pos = 19
    moves_list = []

    def get_moves(_game_lines):
        if "HA[" in _game_lines[0]:
            handicap = int(_game_lines[0].split("HA[")[1][0])
        else:
            handicap = 0
        _move_list = []
        const = 4
        for row in _game_lines[1:-1]:
            x = translate(row[3])
            y = translate(row[4])
            if row[1] + row[2] == "AB":
                for i in range(handicap):
                    x = translate(row[4 + (i * const)])
                    y = translate(row[5 + (i * const)])
                    _move = ["b", x, y]
                    if x != total_pos and y != total_pos:
                        _move_list.append(_move)
            else:
                if row[1] == "B":
                    _move = ["b", x, y]
                if row[1] == "W":
                    _move = ["w", x, y]
                if x != total_pos and y != total_pos:
                    _move_list.append(_move)
        return _move_list

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

    counter = 1
    total_files = len(glob.glob(os.path.join(original_path, '*.sgf')))
    for infile in glob.glob(os.path.join(original_path, '*.sgf')):
        start_time = time.time()
        file = open(infile, 'r', encoding="ISO-8859-1")
        file_lines = file.readlines()
        moves_list.append(len(get_moves(file_lines)))
        print(infile)
        print("Getting moves from file ", counter, "out of", total_files,
              "files. ............................................... ",
              round((counter / total_files * 100), 2), "% ............................................... ",
              round((time.time() - start_time) * 1000, 2), "ms", "\n")
        counter = counter + 1
        file.close()

    unique_moves_list, unique_moves_list_count = np.unique(moves_list, return_counts=True)
    print(unique_moves_list, "\n")
    print(unique_moves_list_count, "\n")
    total_data = sum(unique_moves_list_count)
    for x, y in np.nditer([unique_moves_list, unique_moves_list_count]):
        print("Moves: %d : Amount: %d, %d %%" % (int(x), int(y), ((int(y)*100)/total_data)))
    print("\n")
    print("Unique Move lengths:", len(unique_moves_list))


# -----------------------------------------------
# .................. MAIN .......................
# -----------------------------------------------
if run_programs[0]:
    check_handicap()
if run_programs[1]:
    check_duplication()
if run_programs[2]:
    get_result_ratio()
if run_programs[3]:
    check_moves()
if run_programs[4]:
    remove_empty_lines()
