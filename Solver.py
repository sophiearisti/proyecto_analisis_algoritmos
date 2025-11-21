## =========================================================================
## Algoritmo Flow Free con Inmutabilidad (Copia del Tablero en cada Paso)
## =========================================================================
import utils 
import time

class Solver:
    
    board = None

    def __init__(self, board):
        self.board = board

    # --------------------------------------------------
    # Iniciar proceso recursivo
    # --------------------------------------------------
    def solve(self):
        # 1. Heurística: ordenar las letras por distancia entre inicio y final
        letters_queue = list(self.board.letters.keys())
        letters_queue.sort(
            key=lambda L: utils.distance(self.board.letters[L][0],
                                         self.board.letters[L][1])
        )
        print(f"Orden de letras a evaluar: {letters_queue}")
        
        # Inicia la recursión con una copia del tablero y el estado inicial (state = None)
        return self._solve_recursive(self.board.copy(), letters_queue, None)

    # --------------------------------------------------
    # Función recursiva principal (DFS con Inmutabilidad)
    # --------------------------------------------------
    def _solve_recursive(self, board, letters_queue, state):
        
        # --- 1. Caso Base y Transición de Color ---

        # Caso base: todos los colores conectados y tablero completo
        if board.is_complete():
            self.board = board
            return True

        # Transición: Elegir el siguiente color si se terminó el anterior (state is None)
        if state is None: 
            if not letters_queue:
                return False  # No más letras en la cola

            # Solo miramos la primera letra, NO la eliminamos de la cola AÚN.
            letter = letters_queue[0]
            start, end = board.letters[letter]
            
            # Establecer el estado inicial (current = start)
            state = {
                "letter": letter,
                "current": start,
                "end": end,
            }

        # --- 2. Expansión de la Ruta (DFS) ---

        cx, cy = state["current"]
        ex, ey = state["end"]

        # Identificar vecinos válidos (libres o destino)
        neighbors = [
            (nx, ny)
            for (nx, ny) in utils.get_non_diagonal_neighbors(cx, cy, board.width, board.height)
            # Válido si es un espacio vacío (' ') O el destino
            if board.get_cell(nx, ny) == " " or (nx, ny) == (ex, ey)
        ]


        # Heurística: Ordenar por distancia al endpoint
        neighbors.sort(key=lambda pos: utils.distance(pos, (ex, ey), board, state["letter"]))

        # --- 3. Intentar cada Vecino (Backtracking implícito) ---
        for nx, ny in neighbors:

            is_destination = (nx, ny) == (ex, ey)
            original_val = board.get_cell(nx, ny)

            # Crear la copia del tablero ANTES de aplicar el movimiento
            new_board = board.copy() 

            # A. Aplicar el Movimiento a la NUEVA copia
            # Solo marcamos si es celda vacía y no el destino.
            if not is_destination and original_val == " ":
                new_board.set_cell(nx, ny, state["letter"])
                
            #print(f"Colocando '{state['letter']}' en ({nx}, {ny})")
           # print(new_board)
            #time.sleep(0.3)  

            # B. Definir Argumentos de la Siguiente Llamada Recursiva
            if is_destination:
                # ÉXITO: La letra se considera resuelta, pasamos a la siguiente.
                next_letters_queue = letters_queue[1:] 
                next_state = None 
            else:
                # INTERMEDIO: La cola de letras NO cambia, avanzamos la ruta.
                next_letters_queue = letters_queue 
                next_state = {
                    "letter": state["letter"],
                    "current": (nx, ny),
                    "end": state["end"],
                }

            # C. Llamada Recursiva
            # Pasamos la nueva copia del tablero.
            if self._solve_recursive(new_board, next_letters_queue, next_state):
                return True

        return False