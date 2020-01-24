# -----------------------------------------------
# ................. LIBRARIES ...................
# -----------------------------------------------


import numpy as np


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
    unique_list = np.unique(original_list)
    print("Unique List Length:", len(unique_list))
    print("Difference:", len(original_list) - len(unique_list))


# -----------------------------------------------
# .................. MAIN .......................
# -----------------------------------------------
# check_handicap()
check_duplication()

file.close()
