import gomill.boards
import gomill.ascii_boards

board_size = 9
board = ['w', '.', 'w', 'w', '.', 'w', 'w', '.', 'w', 'w', 'w', '.', 'w', 'w', 'w', '.', 'w', '.', 'w', '.', 'w', '.', 'w', 'w', 'w', '.', 'w', 'w', 'w', 'w', 'w', 'b', 'w', 'b', 'w', 'w', 'w', 'w', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'w', 'b', 'b', '.', '.', '.', 'b', 'b', '.', 'b', 'b', 'b', 'b', 'b', '.', 'b', '.', '.', 'b', 'b', 'b', '.', 'b', '.', 'b', '.', '.', '.', '.', '.', 'b', '.', 'b', '.', 'b', '.']
board188 = ['.', 'b', 'b', 'w', '.', 'b', 'b', '.', '.', 'b', '.', '.', '.', 'b', 'b', 'b', '.', '.', '.', 'b', 'b', '.', '.', 'b', 'b', 'b', 'b', 'b', '.', 'b', 'b', '.', 'b', 'w', 'b', 'w', 'b', 'b', '.', 'b', 'b', 'w', 'w', 'w', 'w', 'w', 'b', 'b', 'b', 'b', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'b', 'w', 'w', 'w', '.', 'w', 'w', 'w', 'w', 'w', '.', 'w', '.', 'w', '.', 'b', 'w', 'w', '.', 'w', 'w', 'w', 'w']
komi = 7


def init_board():
    global end_board
    mainTab = []
    for i in range(board_size):
        tempTab = []
        for i in range(board_size):
            tempTab.append("+")
        mainTab.append(tempTab)
    return mainTab

def play(_turn):
    global game_board
    x = _turn[1]
    y = _turn[2]
    color = _turn[0]
    game_board.play(x, y, color)

def translate(board):
    _move_list = []
    for i in range(len(board)):
        x = i%9
        y = i/9
        y = str(int(y))
        y = y[0]
        y = int(y)
        print(x)
        print(y)
        if board[i] == "b" or board[i] == "B":
            _move = ["b", x, y]
            _move_list.append(_move)
        if board[i] == "w" or board[i] == "W":
            _move = ["w", x, y]
            _move_list.append(_move)
    return _move_list
game_board = gomill.boards.Board(board_size)
initboard = init_board()
movelist = translate(board188)
for i in movelist:
    play(i)

#play(["b", 2,1])
area_score = game_board.area_score() - komi
print("Area Score:", area_score, "\n")
play(["b", 2,1])
area_score = game_board.area_score() - komi
print("Area Score:", area_score, "\n")
