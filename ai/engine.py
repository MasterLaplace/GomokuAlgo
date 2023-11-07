class Brain:
    def __init__(self, player, depth):
        self.player = player
        self.opponent = "X" if player == "O" else "O"
        self.depth = depth

    def minimax(self, board, depth, maximizing_player):
        if depth == 0 or self.check_winner(board):
            return self.evaluate_board(board)

        if maximizing_player:
            max_eval = float('-inf')
            for move in self.get_possible_moves(board):
                board[move[0]][move[1]] = self.player
                eval = self.minimax(board, depth - 1, False)
                max_eval = max(max_eval, eval)
                board[move[0]][move[1]] = " "
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.get_possible_moves(board):
                board[move[0]][move[1]] = self.opponent
                eval = self.minimax(board, depth - 1, True)
                min_eval = min(min_eval, eval)
                board[move[0]][move[1]] = " "
            return min_eval

    def make_best_move(self, board):
        best_move = None
        best_eval = float('-inf')
        for move in self.get_possible_moves(board):
            board[move[0]][move[1]] = self.player
            eval = self.minimax(board, self.depth, False)
            board[move[0]][move[1]] = " "
            if eval > best_eval:
                best_eval = eval
                best_move = move
        return best_move
    
    def get_possible_moves(self, board):
        moves = []
        for i in range(20):
            for j in range(20):
                if board[i][j] == " ":
                    moves.append((i, j))
        return moves

    def evaluate_board(self):
        return 0
    
    def check_winner(self):
        return False