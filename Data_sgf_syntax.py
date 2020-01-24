import os
import glob
import time

directory_path = "Data/Original/foxwq_Pro-9d/*"
board_size = 19
total_pos = 19


def convert(_data):
    result = _data[0].split(";")
    output.write(result[0] + ";" + result[1] + "\n")
    for i in range(len(result)):
        if i >= 2:
            output.write(";" + result[i] + "\n")


time_start = time.time()
print("Starting at " + time.strftime("%Y-%m/%d--%H-%M-%S"), "\n")
counter = 1
total_files = len(glob.glob(os.path.join(directory_path, '*.sgf')))
for infile in glob.glob(os.path.join(directory_path, '*.sgf')):
    start_time = time.time()
    file = open(infile, 'r', encoding="ISO-8859-1")
    lines = file.readlines()
    file.close()
    output = open(infile, 'w', encoding="ISO-8859-1")
    convert(lines)
    output.close()
    print("Converting file", counter, "out of", total_files, "files. .................. ",
          round((counter / total_files * 100), 2), "% ..................",
          round((time.time() - start_time) * 1000, 2), "ms")
    counter = counter + 1


print("Stopping at " + time.strftime("%Y-%m/%d--%H-%M-%S"), "\n")
print("It took ", round((time.time() - time_start) / 60, 2), "minutes")
