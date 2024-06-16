def stockfish_score(self, board,  color, depth=10):
        with chess.engine.SimpleEngine.popen_uci('/content/stockfish') as sf:
            result = sf.analyse(board, chess.engine.Limit(depth=depth))
            if color == 'white':
                return result['score'].white().score()
            return result['score'].black().score()

def stockfish(self, board, depth, maximizing, alpha, beta):
    if depth == 0:
        return self.static_eval(board), None

    # white
    if maximizing:
        best_move = None
        max_eval = -math.inf
        moves = self.get_moves(board, 'white')
        print(moves)
        for move in moves:
            self.explored += 1
            piece = board.squares[move.initial_square.row][move.initial_square.col].piece
            temp_board = copy.deepcopy(board)
            temp_board.move(piece, move)
            piece.moved = False
            eval = self.stockfish_score(temp_board, color='white', depth=10)
            if eval > max_eval:
                max_eval = eval
                best_move = move

            alpha = max(alpha, max_eval)
            if beta <= alpha: break

        if len(moves) == 0:
            self.checkmate = True

        if not best_move and len(moves) != 0:
            best_move = moves[0]

        return max_eval, best_move

    # black
    elif not maximizing:
        best_move = None
        min_eval = math.inf
        moves = self.get_moves(board, 'black')
        for move in moves:
            self.explored += 1
            piece = board.squares[move.initial_square.row][move.initial_square.col].piece
            temp_board = copy.deepcopy(board)
            temp_board.move(piece, move)
            piece.moved = False
            eval = self.stockfish_score(temp_board, color='black', depth=10)
            if eval < min_eval:
                min_eval = eval
                best_move = move

            beta = min(beta, min_eval)
            if beta <= alpha: break


        if len(moves) == 0:
            self.checkmate = True

        if not best_move and len(moves) != 0:
            best_move = moves[0]

        return min_eval, best_move
