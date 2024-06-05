from square import Square
from move import Move
from piece import Bishop, Pawn, King, Knight, Queen, Rook
from const import WIDTH, HEIGHT, ROWS, COLS, SQSIZE


class Board:
    def __init__(self) -> None:
        self.squares = [[0,0,0,0,0,0,0,0] for col in range(COLS)]
        self.last_move = None
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')
    
    def move(self, piece, move):
        initial_position = move.initial_square
        final_position = move.final_square

        # debug info wit hconsole move update
        self.squares[initial_position.row][initial_position.row].piece = None
        self.squares[final_position.row][final_position.col].piece = piece

        # move
        piece.moved = True

        # clear valid moves
        piece.clear_moves()

        # set last move
        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves
    
    def calc_moves(self, piece, row, col):
        if isinstance(piece, Pawn):
            self._pawn_moves(piece, row, col)

        elif isinstance(piece, Knight):
            self._knight_moves(piece, row, col)

        elif isinstance(piece, Bishop):
            self._bishop_moves(piece, row, col)

        elif isinstance(piece, Rook):
            self._rook_moves(piece, row, col)

        elif isinstance(piece, Queen):
            self._queen_moves(piece, row, col)

        elif isinstance(piece, King):
            self._king_moves(piece, row, col)
    
    def _pawn_moves(self, piece, row, col):
        steps = 1 if piece.moved else 2

        # vertical moves
        start = row + piece.dir
        end = row + (piece.dir * (1 + steps))
        for possible_move_row in range(start, end, piece.dir):
            if Square.in_range(possible_move_row):
                if self.squares[possible_move_row][col].isempty():
                    initial_square = Square(row, col)
                    final_square = Square(possible_move_row, col)
                    move = Move(initial_square, final_square)
                    piece.add_moves(move)
                else:
                    break
            else:
                break

        # diagonal moves
        possible_move_row = row + piece.dir
        possible_move_cols = [col-1, col+1]
        for possible_move_col in possible_move_cols:
            if Square.in_range(possible_move_row, possible_move_col):
                if self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                    initial_square = Square(row, col)
                    final_square = Square(possible_move_row, possible_move_col)
                    move = Move(initial_square, final_square)
                    piece.add_moves(move)

    def _knight_moves(self, piece, row, col):
        # 8 positions
        possible_moves = [
            (row-2, col+1),
            (row-2, col-1),
            (row-1, col+2),
            (row-1, col-2),
            (row+2, col+1),
            (row+2, col-1),
            (row+1, col+2),
            (row+1, col-2)
        ]

        for possible_move in possible_moves:
            possible_move_row, possible_move_col = possible_move
        
            if Square.in_range(possible_move_row, possible_move_col):
                if self.squares[possible_move_row][possible_move_col].isempy_or_rival(piece.color):
                    initial_square = Square(row, col)
                    final_square = Square(possible_move_row, possible_move_col)
                    move = Move(initial_square, final_square)
                    piece.add_moves(move)

    def _bishop_moves(self, piece, row, col):
        incrs = [
            (-1, 1),
            (-1, -1),
            (1, 1,),
            (1, -1)
        ]
        self._straight_moves(piece, row, col, incrs)

    def _rook_moves(self, piece, row, col):
        incrs = [
            (-1, 0),
            (0, 1),
            (1, 0),
            (0, -1)
        ]
        self._straight_moves(piece, row, col, incrs)

    def _queen_moves(self, piece, row, col):
        incrs = [
            (-1, 1),
            (-1, -1),
            (1, 1,),
            (1, -1),
            (-1, 0),
            (0, 1),
            (1, 0),
            (0, -1)
        ]
        self._straight_moves(piece, row, col, incrs)

    def _king_moves(self, piece, row, col):
        pass
    
    def _straight_moves(self, piece, row, col, incrs):
        for incr in incrs:
            row_incr, col_incr = incr
            possible_move_row = row + row_incr
            possible_move_col = col + col_incr

            if Square.in_range(possible_move_row, possible_move_col):
                initial_square = Square(row, col)
                final_square = Square(possible_move_row, possible_move_col)
                move = Move(initial_square, final_square)

                if self.squares[possible_move_row][possible_move_col].isempty():
                    piece.add_moves(move)
                    
                if self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                    piece.add_moves(move)
                    break

                if self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                    piece.add_moves(move)
                    break

            else:
                break
                
            possible_move_row = possible_move_row + row_incr
            possible_move_col = possible_move_col + row_incr

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))
        
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))
        
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))
        
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        self.squares[row_other][4] = Square(row_other, 4, King(color))
        