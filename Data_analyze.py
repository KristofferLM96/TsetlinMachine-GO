# -----------------------------------------------
# ................. LIBRARIES ...................
# -----------------------------------------------


import numpy as np
# import random


# -----------------------------------------------
# ............. GLOBAL VARIABLES ................
# -----------------------------------------------

# 9x9Natsukaze || 9x9_10k_r104_144x20k
name = "9x9_10k_r104_144x20k"
file_name = name + "_binary.txt"
path = "Data/Binary/" + file_name
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


# -----------------------------------------------
# .................. MAIN .......................
# -----------------------------------------------
# check_handicap()
# check_duplication()
get_result_ratio()
