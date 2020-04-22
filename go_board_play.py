import gomill.boards
import gomill.ascii_boards
def go_calc(board):
    board_size = 9
    komi = 7
    def get_board(game_board):
        end_board = []
        for y in range(board_size):
            for x in range(board_size):
                pos = game_board.get(x, y)
                if pos == "w" or pos == "b" or pos == "W" or pos == "B":
                    end_board.append(pos)
                else:
                    end_board.append(".")
        return end_board
    def play(_turn,game_board):
        x = _turn[1]
        y = _turn[2]
        color = _turn[0]
        game_board.play(x, y, color)
        return game_board
    def translate(board):
        _move_list = []
        for i in range(len(board)):
            x = i % 9
            y = i / 9
            y = str(int(y))
            y = y[0]
            y = int(y)
            if board[i] == "b" or board[i] == "B":
                _move = ["b", x, y]
                _move_list.append(_move)
            if board[i] == "w" or board[i] == "W":
                _move = ["w", x, y]
                _move_list.append(_move)
        return _move_list
    game_board = gomill.boards.Board(board_size)
    movelist = translate(board)
    for i in movelist:
        game_board = play(i,game_board)
    area_score = game_board.area_score() - komi
    newbwboard = get_board(game_board)
    return area_score, newbwboard