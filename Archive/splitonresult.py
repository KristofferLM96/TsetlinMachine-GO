import csv
gowin = open("GoWin9x9.txt",'w')
goloss = open("GoLoss9x9.txt",'w')
godraw = open("GoDraw9x9.txt",'w')

def convert(input):
    rows = ''
    i=0
    while i < len(input)-1:
        rows =rows+ input[i]+","
        i+=1
    if input[len(input)-1] == "1":
        rows = rows + "1\n"
        gowin.write(rows)
    elif input[len(input)-1] == "0":
        rows = rows + "0\n"
        goloss.write(rows)
    else:
        rows = rows + "2\n"
        godraw.write(rows)

with open("9x9binary.txt", newline='') as File:
    reader =csv.reader(File)
    for row in reader:
        convert(row)
File.close()
gowin.close()
goloss.close()
godraw.close()