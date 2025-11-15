# calcular distancia euclidiana entre dos puntos
def distance(pos1, pos2):
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5

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