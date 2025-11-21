import random
import copy
import time
from collections import deque

class NumberlinkGA:
    def __init__(self, input_file):
        self.rows = 0
        self.cols = 0
        self.grid_layout = []
        self.endpoints = {} 
        self.population_size = 100 
        self.mutation_rate = 0.4   
        self.parse_input(input_file)
        
    def parse_input(self, file_path):
        with open(file_path, 'r') as f:
            lines = f.readlines()
            dims = lines[0].strip().split()
            self.rows = int(dims[0])
            self.cols = int(dims[1])
            
            self.grid_layout = []
            for r, line in enumerate(lines[1:]):
                row_data = list(line.replace('\n', ''))
                # Normalizar longitud de línea
                if len(row_data) < self.cols:
                    row_data += [' '] * (self.cols - len(row_data))
                # Recortar si sobra (espacios extra al final)
                row_data = row_data[:self.cols]
                
                self.grid_layout.append(row_data)
                
                for c, char in enumerate(row_data):
                    if char != ' ' and char.strip() != '': # Ignorar caracteres invisibles raros

                        clean_char = char
                        if clean_char not in self.endpoints:
                            self.endpoints[clean_char] = []
                        self.endpoints[clean_char].append((r, c))

    def get_path_bfs(self, start, end, obstacles):
        """Busca camino simple de start a end."""
        return self._bfs_search(start, end, obstacles)

    def get_path_via_waypoint(self, start, end, waypoint, obstacles):
        """
        Intenta ir de Start -> Waypoint -> End.
        Esto fuerza al camino a dar una vuelta larga para ocupar espacio.
        """
        # 1. Camino Start -> Waypoint
        path1 = self._bfs_search(start, waypoint, obstacles)
        if not path1: return None
        
        # 2. Añadir path1 a obstáculos para que path2 no se cruce a sí mismo
        new_obstacles = obstacles.copy()
        for p in path1:
            new_obstacles.add(p)
            
        # 3. Camino Waypoint -> End
        path2 = self._bfs_search(waypoint, end, new_obstacles)
        if not path2: return None
        
        # Unir caminos (path1 termina en waypoint, path2 empieza en waypoint)
        return path1[:-1] + path2

    def _bfs_search(self, start, end, obstacles):
        """Motor de búsqueda BFS con aleatoriedad en dirección."""
        queue = deque([(start, [start])])
        visited = set([start])
        visited.update(obstacles) # Marcar obstáculos como visitados
        
        # Si el destino es un obstáculo (ej. endpoint mal marcado), permitir llegar
        if end in visited:
            visited.remove(end)

        while queue:
            (r, c), path = queue.popleft()
            
            if (r, c) == end:
                return path
            
            # Aleatorizar direcciones para que no siempre pegue arriba-izquierda
            moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            random.shuffle(moves)
            
            for dr, dc in moves:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    if (nr, nc) not in visited:
                        visited.add((nr, nc))
                        queue.append(((nr, nc), path + [(nr, nc)]))
        return None

    def generate_individual(self):
        individual = {}
        # Orden aleatorio para que no siempre el primer color tome el camino fácil
        colors = list(self.endpoints.keys())
        random.shuffle(colors)
        
        used_cells = set()
        
        for color in colors:
            start, end = self.endpoints[color][0], self.endpoints[color][1]
            # Intentamos conectar respetando lo que ya pusieron los otros colores
            path = self.get_path_bfs(start, end, used_cells)
            
            if path:
                individual[color] = path
                for cell in path:
                    used_cells.add(cell)
            else:
                individual[color] = [] # Camino roto inicial
        return individual

    def calculate_fitness(self, individual):
        grid_usage = {}
        collisions = 0
        broken_paths = 0
        total_path_cells = 0
        
        # 1. Analizar caminos
        for color, path in individual.items():
            if not path:
                broken_paths += 1
                continue
            
            # Validar integridad
            start, end = self.endpoints[color][0], self.endpoints[color][1]
            if path[0] != start or path[-1] != end:
                broken_paths += 1 # Penalización extra por camino corrupto
            
            for cell in path:
                total_path_cells += 1
                grid_usage[cell] = grid_usage.get(cell, 0) + 1

        # 2. Calcular Colisiones
        for cell, count in grid_usage.items():
            if count > 1:
                collisions += (count - 1)
        
        # 3. Calcular Vacíos (CRÍTICO PARA TU PROBLEMA)
        total_cells = self.rows * self.cols
        # Celdas ocupadas validamente (al menos una vez)
        occupied_count = len(grid_usage)
        empty_cells = total_cells - occupied_count
        
        # PESOS AJUSTADOS:
        # Prioridad 1: No roturas (10000)
        # Prioridad 2: No colisiones (1000)
        # Prioridad 3: LLENAR EL TABLERO (50 por cada celda vacía) -> Esto fuerza la expansión
        return (broken_paths * 10000) + (collisions * 1000) + (empty_cells * 50)

    def mutate(self, individual):
        """
        Mutación Mejorada:
        1. Intenta reconectar normal.
        2. O intenta expandir hacia un espacio vacío (Waypoint).
        """
        colors = list(self.endpoints.keys())
        target_color = random.choice(colors)
        
        # Definir obstáculos (todos los otros caminos)
        obstacles = set()
        for color, path in individual.items():
            if color != target_color:
                for cell in path:
                    obstacles.add(cell)
        
        start, end = self.endpoints[target_color][0], self.endpoints[target_color][1]
        
        # ESTRATEGIA DE MUTACIÓN
        # 50% de probabilidad: Buscar camino simple (optimización)
        # 50% de probabilidad: Buscar camino expansivo (llenado)
        
        new_path = None
        
        if random.random() < 0.5:
            # Búsqueda simple
            new_path = self.get_path_bfs(start, end, obstacles)
        else:
            # Búsqueda expansiva: Buscar una celda vacía en el tablero
            # Calcular celdas vacías actuales considerando obstáculos
            all_cells = set((r, c) for r in range(self.rows) for c in range(self.cols))
            empty_cells = list(all_cells - obstacles)
            
            if empty_cells:
                # Elegir 3 candidatos y probar (para no tardar tanto)
                candidates = random.sample(empty_cells, min(3, len(empty_cells)))
                for waypoint in candidates:
                    if waypoint == start or waypoint == end: continue
                    # Intentar forzar paso por waypoint
                    p = self.get_path_via_waypoint(start, end, waypoint, obstacles)
                    if p:
                        new_path = p
                        break
                # Si fallan los waypoints, intentar normal
                if not new_path:
                    new_path = self.get_path_bfs(start, end, obstacles)
            else:
                new_path = self.get_path_bfs(start, end, obstacles)

        if new_path:
            individual[target_color] = new_path
        
        return individual

    def crossover(self, parent1, parent2):
        child = {}
        colors = list(self.endpoints.keys())
        # Cruce Uniforme
        for color in colors:
            # Heredar gen
            gene = parent1.get(color, []) if random.random() > 0.5 else parent2.get(color, [])
            child[color] = copy.deepcopy(gene)
        return child

    def print_board(self, individual):
        display_grid = [[' ' for _ in range(self.cols)] for _ in range(self.rows)]
        for color, path in individual.items():
            for (r, c) in path:
                display_grid[r][c] = color
        
        output = []
        for row in display_grid:
            output.append("".join(row))
        return "\n".join(output)

    def solve(self, max_seconds=30):
        population = [self.generate_individual() for _ in range(self.population_size)]
        start_time = time.time()
        generation = 0
        
        while True:
            population.sort(key=self.calculate_fitness)
            best_fitness = self.calculate_fitness(population[0])
            
            if generation % 50 == 0:
                print(f"Gen {generation} | Fitness: {best_fitness}")
            
            # Condición de éxito estricta: 0 errores
            if best_fitness == 0:
                print(f"\n¡SOLUCIÓN PERFECTA ENCONTRADA! (Gen {generation})")
                break
            
            # Timeout
            if time.time() - start_time > max_seconds:
                print("\nTiempo límite alcanzado.")
                break
            
            # Elitismo y Reproducción
            next_gen = population[:10] # Guardar los 10 mejores
            
            while len(next_gen) < self.population_size:
                # Torneo
                sample = random.sample(population[:50], 5)
                sample.sort(key=self.calculate_fitness)
                p1, p2 = sample[0], sample[1]
                
                child = self.crossover(p1, p2)
                if random.random() < self.mutation_rate:
                    child = self.mutate(child)
                next_gen.append(child)
            
            population = next_gen
            generation += 1
        
        best_sol = population[0]
        print("\n--- Tablero Resuelto ---")
        print(self.print_board(best_sol))

if __name__ == "__main__":
    # Archivo temporal con tu ejemplo difícil
    import os
    filename = "tablero_dificil.txt"
    with open(filename, "w") as f:
        f.write("8 8\n")
        f.write("        \n")
        f.write(" m  1 1 \n")
        f.write("  2     \n")
        f.write("  m 3v  \n")
        f.write("r 2  n  \n")
        f.write("a 3nv   \n")
        f.write("ra      \n")
        f.write("        \n")

    # Ejecutar con un poco más de tiempo por la complejidad
    solver = NumberlinkGA(filename)
    solver.solve(max_seconds=60)