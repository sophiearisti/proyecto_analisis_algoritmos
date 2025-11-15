## =========================================================================
## @authors Isaac Janica, Sophia Aristizabal
## =========================================================================

## =========================================================================
## MANUAL DE USO 
## Este es el archivo principal que ejecuta el juego de buscaminas.
## Se debe ejecutar desde la terminal de la siguiente manera:
## python3 MineSweeper.py width height mines player <arguments>
## donde:
## - width: ancho del tablero (numero de columnas)
## - height: alto del tablero (numero de filas) 
## - mines: numero de minas
## - player: archivo del jugador (por ejemplo, code/Player/Random.py)

## Para poder utilizar el codigo, es necesario tener instaladas las siguientes
## librerias de Python:
## - pandas
## - numpy
## - scikit-learn
## =========================================================================


import importlib.util, sys
from Board import *
from Solver import *

if __name__ == "__main__":
    # Lectura de argumentos
    if len(sys.argv) < 2:
        print("Usage: python3  FlowFree.py <filename>.txt")
        sys.exit(1)

    filename = sys.argv[1]
    
    # Crear el tablero
    board = Board(filename)
    
    print(board)
    
    # Crear el solver
    
    solver = Solver(board)
    
    # Resolver el tablero
    if solver.solve():
        print("Solucionado! :D")
        print(board)
    else:
        print("No se encontró solución :( .")