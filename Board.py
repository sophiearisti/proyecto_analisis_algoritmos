## =========================================================================
## Rpresentaci'on del tablero del juego Flow Free
## =========================================================================

class Board:
    
    grid = []
    
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
                
                # Guardar cada carácter en el grid (incluyendo espacios)
                for x in range(self.width):
                    self.grid[x][y] = line[x]
        
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
