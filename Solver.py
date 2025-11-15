## =========================================================================
## Algoritmo que soluciona recursivamente el juego Flow Free
## Este encuentra la solucion del tablero utilizando backtracking
## =========================================================================

class Solver:
    
    board = None
    
    def __init__(self, board):
        self.board = board
    
    def solve(self):
        # Implementar el algoritmo de solucion aqui
        return self.board.is_complete()