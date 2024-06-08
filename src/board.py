from square import Square
from move import Move
from piece import Bishop, Pawn, King, Knight, Queen, Rook
from const import WIDTH, HEIGHT, ROWS, COLS, SQSIZE
import copy



class Board:
    def __init__(self) -> None:
        self.squares = [[0,0,0,0,0,0,0,0] for col in range(COLS)]
        self.last_move = None
        self.checkmate = False
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')
    
    def check_checkmate(self):
        return self.checkmate
    
    def move(self, piece, move):
        initial_square = move.initial_square
        final_square = move.final_square

        en_passant_empty = self.squares[final_square.row][final_square.col].isempty()

        # debug info with console move update
        self.squares[initial_square.row][initial_square.col].piece = None
        self.squares[final_square.row][final_square.col].piece = piece

        if isinstance(piece, Pawn):
            # en passant capture
            diff = final_square.col - initial_square.col
            if diff != 0 and en_passant_empty:
                # console board move update
                self.squares[initial_square.row][initial_square.col + diff].piece = None
                self.squares[final_square.row][final_square.col].piece = piece
            
            # pawn promotion
            else:
                self.check_promotion(piece, final_square)

        # king castling
        if isinstance(piece, King):
            if self.castling(initial_square, final_square):
                diff = final_square.col - initial_square.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moves[-1])

        # move
        piece.moved = True

        # clear valid moves
        piece.clear_moves()

        # set last move
        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves
    
    def set_true_en_passant(self, piece):
        
        if not isinstance(piece, Pawn):
            return

        for row in range(ROWS):
            for col in range(COLS):
                if isinstance(self.squares[row][col].piece, Pawn):
                    self.squares[row][col].piece.en_passant = False
        
        piece.en_passant = True

    def in_check(self, piece, move, bool):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move)
        
        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_rival_piece(piece.color):
                    p = temp_board.squares[row][col].piece 
                    temp_board.calc_moves(p, row, col, bool=False)
                    for m in p.moves:
                        if isinstance(m.final_square.piece, King):
                            return True
        
        return False
    
    
    def check_promotion(self, piece, final_position):
        if final_position.row == 0 or final_position.row == 7:
            self.squares[final_position.row][final_position.col].piece = Queen(piece.color)

    def castling(self, initial_position, final_position):
        return abs(initial_position.col - final_position.col) == 2
    
    def calc_moves(self, piece, row, col, bool=True):
        """responsible for all possible moves for specific figure"""
        if isinstance(piece, Pawn):
            self._pawn_moves(piece, row, col, bool)

        elif isinstance(piece, Knight):
            self._knight_moves(piece, row, col, bool)

        elif isinstance(piece, Bishop):
            self._bishop_moves(piece, row, col, bool)

        elif isinstance(piece, Rook):
            self._rook_moves(piece, row, col, bool)

        elif isinstance(piece, Queen):
            self._queen_moves(piece, row, col, bool)

        elif isinstance(piece, King):
            self._king_moves(piece, row, col, bool)
    
    def _pawn_moves(self, piece, row, col, bool=True):
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

                    # check potencial checks
                    if bool:
                        if not self.in_check(piece, move, bool):
                            piece.add_moves(move)
                    else:
                        piece.add_moves(move)
                else: break
            else: 
                self.checkmate = True

        # diagonal moves
        possible_move_row = row + piece.dir
        possible_move_cols = [col-1, col+1]

        for possible_move_col in possible_move_cols:
            if Square.in_range(possible_move_row, possible_move_col):
                if self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                    initial_square = Square(row, col)
                    final_piece = self.squares[possible_move_row][possible_move_col].piece
                    final_square = Square(possible_move_row, possible_move_col, final_piece)
                    move = Move(initial_square, final_square)
                    
                    # check potencial checks
                    if bool:
                        if not self.in_check(piece, move, bool):
                            piece.add_moves(move)
                        else:
                            self.checkmate = True
                    else:
                        piece.add_moves(move)


        # en passant moves
        r = 3 if piece.color == 'white' else 4
        fr = 2 if piece.color == 'white' else 5

        # left en pessant
        if Square.in_range(col-1) and row == r:
            if self.squares[row][col-1].has_rival_piece(piece.color):
                p = self.squares[row][col-1].piece
                if isinstance(p, Pawn):
                    if p.en_passant:
                        initial_square = Square(row, col)
                        final_square = Square(fr, col-1, p)
                        # create a new move
                        move = Move(initial_square, final_square)
                        
                        if bool:
                            if not self.in_check(piece, move, bool):
                                piece.add_moves(move)
                            else:
                                self.checkmate = True
                        else:
                            piece.add_moves(move)
        
        # right en pessant
        if Square.in_range(col+1) and row == r:
            if self.squares[row][col+1].has_rival_piece(piece.color):
                p = self.squares[row][col+1].piece
                if isinstance(p, Pawn):
                    if p.en_passant:
                        initial_square = Square(row, col)
                        final_square = Square(fr, col+1, p)
                        # create a new move
                        move = Move(initial_square, final_square)
                        
                        if bool:
                            if not self.in_check(piece, move, bool):
                                piece.add_moves(move)
                            else:
                                self.checkmate = True
                        else:
                            piece.add_moves(move)

    def _knight_moves(self, piece, row, col, bool=True):
        # 8 available positions for knight
        possible_moves = [
            (row-2, col+1),
            (row-1, col+2),
            (row+1, col+2),
            (row+2, col+1),
            (row+2, col-1),
            (row+1, col-2),
            (row-1, col-2),
            (row-2, col-1),
        ]
        
        # next move should be in possible_move
        for possible_move in possible_moves:
            possible_move_row, possible_move_col = possible_move
        
            if Square.in_range(possible_move_row, possible_move_col):
                if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color):
                    initial_square = Square(row, col)
                    final_piece = self.squares[possible_move_row][possible_move_col].piece
                    final_square = Square(possible_move_row, possible_move_col, final_piece)
                    move = Move(initial_square, final_square)
                     
                    # check potencial checks
                    if bool:
                        if not self.in_check(piece, move, bool):
                            # append new move
                            piece.add_moves(move)
                        else: break
                    else:
                        # append new move
                        piece.add_moves(move)

    def _bishop_moves(self, piece, row, col, bool=True):
        incrs = [
            (-1, 1),
            (-1, -1),
            (1, 1,),
            (1, -1)
        ]
        self._straight_moves(piece, row, col, incrs, bool)

    def _rook_moves(self, piece, row, col, bool=True):
        incrs = [
            (-1, 0),
            (0, 1),
            (1, 0),
            (0, -1)
        ]
        self._straight_moves(piece, row, col, incrs, bool)

    def _queen_moves(self, piece, row, col, bool=True):
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
        self._straight_moves(piece, row, col, incrs, bool)

    def _king_moves(self, piece, row, col, bool=True):
        adjs = [
            (row-1, col+0), # up
            (row-1, col+1), # up-right
            (row+0, col+1), # right
            (row+1, col+1), # down-right
            (row+1, col+0), # down
            (row+1, col-1), # down-left
            (row+0, col-1), # left
            (row-1, col-1), # up-left
        ]

        # normal moves
        for possible_move in adjs:
            possible_move_row, possible_move_col = possible_move

            if Square.in_range(possible_move_row, possible_move_col):
                if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color):
                    initial_square = Square(row, col)
                    final_square = Square(possible_move_row, possible_move_col)
                    move = Move(initial_square, final_square)

                    if bool:
                        if not self.in_check(piece, move, bool):
                            piece.add_moves(move)
                        else: 
                            self.checkmate = True
                    else:
                        piece.add_moves(move)

        # castling moves
        if not piece.moved:
            left_rook = self.squares[row][0].piece
            if isinstance(left_rook, Rook):
                if not left_rook.moved:
                    for c in range(1, 4):
                        # castling is not possible because there are pieces in between 
                        if self.squares[row][c].has_piece():
                            break

                        if c == 3:
                            # adds left rook to king
                            piece.left_rook = left_rook

                            # rook move
                            initial_square = Square(row, 0)
                            final_square = Square(row, 3)
                            moveR = Move(initial_square, final_square)

                            # king move
                            initial_square = Square(row, col)
                            final_square = Square(row, 2)
                            moveK = Move(initial_square, final_square)

                            if bool:
                                if not self.in_check(piece, moveK, bool) and not self.in_check(left_rook, moveR, bool):
                                    left_rook.add_moves(moveR)
                                    piece.add_moves(moveK)
                            else:
                                left_rook.add_moves(moveR)
                                piece.add_moves(moveK)

            # king castling
            right_rook = self.squares[row][7].piece
            if isinstance(right_rook, Rook):
                if not right_rook.moved:
                    for c in range(5, 7):
                        # castling is not possible because there are pieces in between ?
                        if self.squares[row][c].has_piece():
                            break

                        if c == 6:
                            # adds right rook to king
                            piece.right_rook = right_rook

                            # rook move
                            initial_square = Square(row, 7)
                            final_square = Square(row, 5)
                            moveR = Move(initial_square, final_square)

                            # king move
                            initial_square = Square(row, col)
                            final_square = Square(row, 6)
                            moveK = Move(initial_square, final_square)

                            if bool:
                                if not self.in_check(piece, moveK, bool) and not self.in_check(right_rook, moveR, bool):
                                    right_rook.add_moves(moveR)
                                    piece.add_moves(moveK)
                                else:
                                    self.checkmate = True
                            else:
                                right_rook.add_moves(moveR)
                                piece.add_moves(moveK)
    
    def _straight_moves(self, piece, row, col, incrs, bool=True):
        for incr in incrs:
            row_incr, col_incr = incr
            possible_move_row = row + row_incr
            possible_move_col = col + col_incr

            while True:
                if Square.in_range(possible_move_row, possible_move_col):
                    # new square
                    initial_square = Square(row, col)
                    final_piece = self.squares[possible_move_row][possible_move_col].piece
                    final_square = Square(possible_move_row, possible_move_col, final_piece)
                    move = Move(initial_square, final_square)

                    # empty -> continue looping
                    if self.squares[possible_move_row][possible_move_col].isempty():
                        if bool:
                            if not self.in_check(piece, move, bool):
                                piece.add_moves(move)
                            else:
                                self.checkmate = True
                        else:
                            piece.add_moves(move)

                    # if there is rival piece go and break loop
                    elif self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                        if bool:
                            if not self.in_check(piece, move, bool):
                                piece.add_moves(move)
                        else:
                            piece.add_moves(move)
                        break

                    # if has team piece ->  break
                    elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                        break
                
                # not in range -> break
                else: break

                possible_move_row = possible_move_row + row_incr
                possible_move_col = possible_move_col + col_incr

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)
        
        # pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))
        
        # knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))
        
        # bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))
        
        # rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # king
        self.squares[row_other][4] = Square(row_other, 4, King(color))
        