path = "1504341719019999478.sgf"
file = open(path, 'r', encoding="ISO-8859-1")
file_lines = file.readlines()
result = file_lines[0].split("RE")
_handicap = file_lines[0].split("HA[")
print(_handicap)
handicap = _handicap[1][0]
print(handicap)

file.close()
