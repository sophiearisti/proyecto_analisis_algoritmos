# calcular distancia euclidiana entre dos puntos
# calcular distancia manhattan entre dos puntos
# si se pasa un tercer argumento (board, letter), se activa la heurística
def distance(pos1, pos2, board=None, letter=None):
    
    # distancia hacia el objetivo  en distancia de montecarlo
    dist_goal = abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    # --- si no hay heurística extra, devolvemos distancia normal ---
    """   if board is None or letter is None:
        return dist_goal"""

    # --- distancia al resto de celdas ocupadas (queremos MAXIMIZAR) ---
    min_dist = 999999
    for x in range(board.width):
        for y in range(board.height):
            cell = board.get_cell(x, y)
            if cell != " " and cell != letter:
                d = abs(pos1[0] - x) + abs(pos1[1] - y)
                if d < min_dist:
                    min_dist = d

    if min_dist == 999999:
        min_dist = 0

    # peso para cuánto importa alejarse de otros colores
    W = 0.4

    # heurística compuesta — minimizamos este valor
    return dist_goal - W * min_dist


# obtener vecinos validos (dentro del tablero) de una celda
# no se consideran diagonales
def get_non_diagonal_neighbors(x, y, width, height):
    neighbors = []
    if x > 0:
        neighbors.append((x - 1, y))
    if x < width - 1:
        neighbors.append((x + 1, y))
    if y > 0:
        neighbors.append((x, y - 1))
    if y < height - 1:
        neighbors.append((x, y + 1))
    return neighbors

# obtener vecinos validos (dentro del tablero) de una celda
#cuentan los vecinos diagonales
def get_neighbors(x, y, width, height):
    neighbors = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height:
                neighbors.append((nx, ny))
    return neighbors