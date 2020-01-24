# -----------------------------------------------
# ................. LIBRARIES ...................
# -----------------------------------------------


import numpy as np
import random


# -----------------------------------------------
# ............. GLOBAL VARIABLES ................
# -----------------------------------------------


file_name = "9x9Natsukaze_binary.txt"
path = "Data/Binary/" + file_name
encoding = "UTF-8"  # ISO-8859-1 / UTF-8
file = open(path, 'r', encoding=encoding)
unique_list = []
original_list = []


# -----------------------------------------------
# ................. FUNCTIONS ...................
# -----------------------------------------------


def check_handicap():
    file_lines = file.readlines()
    _handicap = file_lines[0].split("HA[")
    print(_handicap)
    handicap = _handicap[1][0]
    print(handicap)


def check_duplication():
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


# -----------------------------------------------
# .................. MAIN .......................
# -----------------------------------------------
# check_handicap()
check_duplication()

file.close()
