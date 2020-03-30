import gomill.boards
import gomill.ascii_boards

board_size = 9
board = ['w', '.', 'w', 'w', '.', 'w', 'w', '.', 'w', 'w', 'w', '.', 'w', 'w', 'w', '.', 'w', '.', 'w', '.', 'w', '.', 'w', 'w', 'w', '.', 'w', 'w', 'w', 'w', 'w', 'b', 'w', 'b', 'w', 'w', 'w', 'w', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'w', 'b', 'b', '.', '.', '.', 'b', 'b', '.', 'b', 'b', 'b', 'b', 'b', '.', 'b', '.', '.', 'b', 'b', 'b', '.', 'b', '.', 'b', '.', '.', '.', '.', '.', 'b', '.', 'b', '.', 'b', '.']
komi = 7

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
def play(_turn):
    global game_board
    x = _turn[1]
    y = _turn[2]
    color = _turn[0]
    game_board.play(x, y, color)
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

get_board()
area_score = game_board.area_score() - komi
print("Area Score:", area_score, "\n")