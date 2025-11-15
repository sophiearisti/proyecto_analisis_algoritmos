## =========================================================================
## Representacion del tablero del juego Flow Free
## =========================================================================
import utils

class Board:
    
    grid = []
    
    letters = {}
    
    width = 0
    height = 0
    
    def __init__(self, filename):
        self.grid = []
        self.load_board(filename)

    def load_board(self, filename):
        # Cargar el tablero desde un archivo de texto
        with open(filename, 'r') as file:
            # la primera linea contiene las dimensiones de esta forma
            # width height
            dimensions = file.readline().strip().split()
            self.width = int(dimensions[0])
            self.height = int(dimensions[1])
            
            print(f"Cargando tablero de {self.width}x{self.height}")
            
            # Inicializar grid
            self.grid = [[None for _ in range(self.height)] for _ in range(self.width)]

            # Leer cada fila del archivo tal cual, manteniendo espacios
            for y in range(self.height):
                line = file.readline().rstrip("\n")

                for x in range(self.width):
                    char = line[x]
                    self.grid[x][y] = char

                    # Si es una letra
                    if char != " ":
                        if char not in self.letters:
                            self.letters[char] = []   # crear lista para esa letra
                        
                        # Registrar la coordenada
                        self.letters[char].append((x, y))

            print(f"Letras y coordenadas encontradas: {self.letters}")

    def __str__(self):
        s = "    "

        # Cabecera de columnas
        for x in range(self.width):
            s += f"+---"
        s += "+\n    "

        for x in range(self.width):
            s += f"| {x} "
        s += "|\n"

        # Filas
        for y in range(self.height):
            # Línea separadora
            s += ""
            for k in range(self.width + 1):
                s += "+---"
            s += "+\n"

            # Contenido de la fila
            s += f"| {chr(ord('A') + y)} "  # Etiqueta A, B, C...
            for x in range(self.width):
                val = self.grid[x][y]
                if val == " ":
                    val = " "   # espacio visible
                s += f"| {val} "
            s += "|\n"

        # Línea final
        for k in range(self.width + 1):
            s += "+---"
        s += "+\n"

        return s
    
    # agragar nueva letra en la posicion x,y
    def set_cell(self, x, y, letter):
        self.grid[x][y] = letter
        
    # obtener el valor en la posicion x,y
    def get_cell(self, x, y):
        return self.grid[x][y]
    
    # eliminar letra en la posicion x,y
    def clear_cell(self, x, y):
        self.grid[x][y] = " "
        
    # tablero completo satisface las condiciones del juego
    def is_complete(self):
        # verificar que no haya espacios vacios
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x][y] == " ":
                    return False
                
        # verificar que todas las letras esten conectadas
        # (esto es una verificacion basica, se asume que el solver
        #  se encarga de conectar las letras correctamente)
        
        # para cada letra en letters 
        # obtener la coordenada de inicio e ir recorriendo arriba o abajo, izquierda o derecha
        # hasta encontrar la otra letra igual 
        # si hay varias posibilidades, seleccionar la que teng menor distancia con la coordenada final
        # se selecciona la siguiente celda en funcion de la distancia euclidiana a la celda final
        # y se sigue con esa asi consecutivamente hasta llegar a la celda final
        # se debe tener en cuenta la celda anterior para no retroceder
        # si se llega a un punto de no retorno y no se llego a la celda final, se retorna falso
        
        for letter, positions in self.letters.items():
            start = positions[0]
            end = positions[1]
            
            current = start
            previous = None
            
            while current != end:
                x, y = current
                neighbors = utils.get_non_diagonal_neighbors(x, y, self.width, self.height)
                
                # filtrar vecinos validos (mismo letter o celda final)
                valid_neighbors = []
                for nx, ny in neighbors:
                    if (nx, ny) == end or self.grid[nx][ny] == letter:
                        valid_neighbors.append((nx, ny))
                
                # eliminar el vecino anterior para no retroceder
                if previous and previous in valid_neighbors:
                    valid_neighbors.remove(previous)
                
                if not valid_neighbors:
                    return False  # no hay camino valido
                
                # seleccionar el vecino mas cercano a la celda final
                next_cell = min(valid_neighbors, key=lambda pos: utils.distance(pos, end))
                
                previous = current
                current = next_cell
        
        return True
    
    def copy(self):
        # Crear board sin llamar al __init__
        new_board = Board.__new__(Board)

        new_board.width = self.width
        new_board.height = self.height

        # Deep copy del grid
        new_board.grid = [row[:] for row in self.grid]

        # Deep copy de letters
        new_board.letters = {
            key: [(x, y) for (x, y) in coords]
            for key, coords in self.letters.items()
        }

        return new_board

