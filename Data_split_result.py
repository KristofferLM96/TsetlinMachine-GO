import csv

name = "9x9Aya"
win = open("Data/Results-Split/" + name + "_win.txt", 'w+')
loss = open("Data/Results-Split/" + name + "_loss.txt", 'w+')
draw = open("Data/Results-Split/" + name + "_draw.txt", 'w+')


def convert(_input):
    rows = ''
    i = 0
    while i < len(_input)-1:
        rows = rows + _input[i]+","
        i += 1
    if _input[len(_input) - 1] == "1":
        rows = rows + "1\n"
        win.write(rows)
    elif _input[len(_input) - 1] == "0":
        rows = rows + "0\n"
        loss.write(rows)
    else:
        rows = rows + "2\n"
        draw.write(rows)


with open("Data/Binary/" + name + "_binary.txt", newline='') as file:
    reader = csv.reader(file)
    for row in reader:
        convert(row)

file.close()
win.close()
loss.close()
draw.close()
