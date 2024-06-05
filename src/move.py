class Move:
    def __init__(self, initial_square, final_square):
        self.initial_square = initial_square
        self.final_square = final_square

    def __str__(self):
        s = ''
        s += f'{self.initial_square.col}, {self.initial_square.row}'
        s += f'-> {self.final_square.col}, {self.final_square.row}'
        return s
    
    def __eq__(self, other):
        return self.initial_square == other.initial_square and self.final_square == other.final_square