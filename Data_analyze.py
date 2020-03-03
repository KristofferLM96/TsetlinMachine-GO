# -----------------------------------------------
# ................. LIBRARIES ...................
# -----------------------------------------------
import glob
import os
import time

import numpy as np
# import random


# -----------------------------------------------
# ............. GLOBAL VARIABLES ................
# -----------------------------------------------

# 9x9Natsukaze || 9x9Aya
name = "9x9Aya"
file_name = name + "_binary.txt"
# path = "Data/Binary/" + file_name
path = "/home/kristoffer/Documents/Data/Original/9x9_10k_r104_144x20k/*"
encoding = "UTF-8"  # ISO-8859-1 / UTF-8
multiple_files = True
unique_list = []
original_list = []

# -----------------------------------------------
# ................. FUNCTIONS ...................
# -----------------------------------------------


def check_handicap():
    file = open(path, 'r', encoding=encoding)
    file_lines = file.readlines()
    _handicap = file_lines[0].split("HA[")
    print(_handicap)
    handicap = _handicap[1][0]
    print(handicap)

    file.close()


def check_duplication():
    file = open(path, 'r', encoding=encoding)
    global original_list
    global unique_list
    original_list = [line.strip() for line in file]
    print("Original List Length:", len(original_list))
    original_length = len(original_list)

    unique_list = np.unique(original_list)
    unique_length = len(unique_list)
    print("Unique List Length:", unique_length)
    print("Original - Unique:", original_length - unique_length, "\n")

    """ Checks whether the random.shuffle() creates duplicates when ran. """
    # random.shuffle(original_list)
    # unique_list = np.unique(original_list)
    # shuffled_length = len(original_list)
    # print("Shuffled List Length:", shuffled_length)
    # unique_length = len(unique_list)
    # print("Unique List Length:", unique_length)
    # print("Shuffled - Unique:", shuffled_length - unique_length, "\n")

    file.close()


def get_result_ratio():
    win = open("Data/Results-Split/" + name + "_win.txt", 'r')
    loss = open("Data/Results-Split/" + name + "_loss.txt", 'r')
    draw = open("Data/Results-Split/" + name + "_draw.txt", 'r')
    win_line = win.readlines()
    loss_line = loss.readlines()
    draw_line = draw.readlines()
    print("Amount of wins: ", len(win_line))
    print("Amount of loss: ", len(loss_line))
    print("Amount of draw: ", len(draw_line))

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
    total_files = len(glob.glob(os.path.join(path, '*.sgf')))
    for infile in glob.glob(os.path.join(path, '*.sgf')):
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
    for game in unique_moves_list:
        print(game)
    print(unique_moves_list)
    print(unique_moves_list_count)


# -----------------------------------------------
# .................. MAIN .......................
# -----------------------------------------------
# check_handicap()
# check_duplication()
# get_result_ratio()
check_moves()
