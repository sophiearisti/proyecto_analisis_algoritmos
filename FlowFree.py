## =========================================================================
## @authors Isaac Janica, Sophia Aristizabal
## =========================================================================

## =========================================================================
## MANUAL DE USO 
## Este es el archivo principal que ejecuta el juego de buscaminas.
## Se debe ejecutar desde la terminal de la siguiente manera:
## python3 FlowFree.py <filename>.txt
## donde:
## - <filename>.txt es el archivo de texto que contiene la representación del tablero.

## Para poder utilizar el codigo, no es necesario instalar librerias externas.
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
        print(solver.board)
    else:
        print("No se encontró solución :( .")
        print(solver.board)