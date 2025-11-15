## =========================================================================
## Algoritmo que soluciona recursivamente el juego Flow Free
## Este encuentra la solucion del tablero utilizando backtracking
## =========================================================================
import utils


class Solver:
    
    board = None

    def __init__(self, board):
        self.board = board

    # --------------------------------------------------
    # Iniciar proceso recursivo
    # --------------------------------------------------
    def solve(self):
        # ordenar las letras a evaluar por distancia entre inicio y final
        letters_queue = list(self.board.letters.keys())
        letters_queue.sort(
            key=lambda L: utils.distance(self.board.letters[L][0],
                                         self.board.letters[L][1])
        )

        return self._solve_recursive(self.board.copy(), letters_queue, None)

    # --------------------------------------------------
    # funcion recursiva
    # --------------------------------------------------
    def _solve_recursive(self, board, letters_queue, state):
        # Si el table está completamente lleno y correctamente lleno
        if board.is_complete():
            self.board = board
            return True

        # State is None → choose next letter
        if state is None or state["current"] == state["end"]:
            if not letters_queue:
                return False  # No hay mas letras para revisar, pero no hay mas para evaluar
                              #Entonces no hay solucion

            # Tomar la siguiente letra (IMPORTANTE: copiar la cola para que funciona el backtracking)
            #falta un copy
            new_queue = letters_queue.copy()
            letter = new_queue.pop(0)

            start, end = board.letters[letter]
            state = {
                "letter": letter,
                "current": start,
                "end": end,
                "previous": None
            }

            # Continue recursion with this letter
            return self._solve_recursive(board, new_queue, state)

        # --------------------------------------------------
        # Expand current letter
        # --------------------------------------------------
        cx, cy = state["current"]
        ex, ey = state["end"]

        # Get empty neighbors
        neighbors = [
            n for n in utils.get_non_diagonal_neighbors(cx, cy, board.width, board.height)
            if board.get_cell(n[0], n[1]) == " "
        ]

        # Sort neighbors by distance to endpoint
        neighbors.sort(key=lambda pos: utils.distance(pos, (ex, ey)))

        # Try each possible neighbor
        for nx, ny in neighbors:

            # CASE 1: movement creates enclosed cell → skip
            if self.creates_enclosed_cell(board, (nx, ny)):
                continue

            # CASE 2: movement blocks some other letter → skip
            if self.blocks_other_letter(board, (nx, ny), state["letter"]):
                continue

            # Try placing the letter here
            new_board = board.copy()
            new_board.set_cell(nx, ny, state["letter"])

            new_state = {
                "letter": state["letter"],
                "current": (nx, ny),
                "end": state["end"],
                "previous": (cx, cy)
            }

            # Recur
            return self._solve_recursive(new_board, letters_queue, new_state)

        return False
    
    ## =========================================================================
    ##  FALTA CORREGIR Y EVALUAR TODA ESTA PARTE
    ## =========================================================================
        
    def evaluarCeldaVacia(self, board, neighbour, value):
        #obtener sus vecinos
        nx, ny = neighbour
        empty_neighbours = [n for n in utils.get_neighbors(nx, ny, board.width, board.height) if board.get_cell(n[0], n[1]) == " "]
        
        #si ese neighbour tiene 2 o mas celdas vacias vecinas
        #no es una celda encerrada
        if len(empty_neighbours) >=2:
            return False
        
        #si esa celda vacia no tiene mas celdas vacias cercanas
        #esta 100% encerrada
        elif len(empty_neighbours) ==0:
            return True
        
        #si solo tiene otra, toca ver si las letras circundantes son de inicio o de fin 
        #si ninguna es de inicio o fin, esta encerrada
        #si por lo menos alguna es de inicio o de fin
            # mirar si no tienen valores iguales circundantes. si todas tienen, esta encerrada
            # si alguna no tiene, puede que no sea un encierro, retornar false
        else:
            filled_neighbours = [n for n in utils.get_non_diagonal_neighbors(nx, ny, board.width, board.height) if board.get_cell(n[0], n[1]) != " "]
            doesntexist = True
            
            for i in filled_neighbours:
                ix, iy = i
                value=board.grid[ix][iy]
                
                if board.letters[value][0] == i:
                    if len([n for n in utils.get_non_diagonal_neighbors(nx, ny, board.width, board.height) if board.get_cell(n[0], n[1]) == value])==0:
                        return False

                elif board.letters[value][1] == i:
                    if len([n for n in utils.get_non_diagonal_neighbors(nx, ny, board.width, board.height) if board.get_cell(n[0], n[1]) == value])==0:
                        return False
 
            return True
            
    
    def evaluarBloqueoLetras(self, board, neighbour, value):
        pass