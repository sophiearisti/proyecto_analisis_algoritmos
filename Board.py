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
        
    def is_complete(self):

        #print("\n=== VERIFICANDO TABLERO COMPLETO ===")

        # Verificar que no haya espacios vacíos
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x][y] == " ":
                    #print(f"[ERROR] Celda vacía encontrada en {(x,y)}")
                    return False

        # Para cada letra, validar su recorrido
        for letter, (start, end) in self.letters.items():
            #print(f"\n>>> VALIDANDO LETRA '{letter}'")
            #print(f"    Start = {start}, End = {end}")

            # Obtener todas las celdas del color
            all_cells = {
                (x, y)
                for x in range(self.width)
                for y in range(self.height)
                if self.grid[x][y] == letter
            }

           # print(f"    Celdas esperadas: {all_cells}")

            # Recorrido DFS/BFS
            visited = []
            stack = [(start, None)]

            #print("    Iniciando recorrido DFS...\n")

            while stack:
                current, previous = stack.pop()
                if current in visited:
                    continue

               # print(f"    Visitando {current}, desde {previous}")
                visited.append(current)

                x, y = current
                neighbors = utils.get_non_diagonal_neighbors(x, y, self.width, self.height)

                for nx, ny in neighbors:
                    if (nx, ny) == end or self.grid[nx][ny] == letter:
                        if (nx, ny) != previous:
                            #print(f"        → Agregando vecino {(nx,ny)} al stack")
                            stack.append(((nx, ny), current))

            #print(f"\n    Recorrido final visitado: {visited}")

            # 2A️⃣ Validar inicio y fin
            if visited[0] != start:
                #print(f"[ERROR] El recorrido NO inicia en start: {start}")
                return False

            if visited[-1] != end:
                #print(f"[ERROR] El recorrido NO termina en end: {end}")
                return False

            # 2B️⃣ Validar que visite todas las celdas del color
            if set(visited) != all_cells:
                #print("[ERROR] Las celdas visitadas NO coinciden con todas las celdas del color")
                #print("        Visitadas:", set(visited))
                #   print("        Esperadas:", all_cells)
                return False

            # 2C️⃣ Verificar continuidad (ningún salto)
            #print("    Verificando continuidad del recorrido...")
            for i in range(len(visited) - 1):
                x1, y1 = visited[i]
                x2, y2 = visited[i + 1]
                if abs(x1 - x2) + abs(y1 - y2) != 1:
                  #  print(f"[ERROR] Discontinuidad entre {visited[i]} y {visited[i+1]}")
                    return False

            #print(f" La letra '{letter}' forma un camino válido y continuo.\n")

        #print(" TODAS las letras forman caminos válidos.")
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

