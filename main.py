import sys
import subprocess

# laberinto_vacio retorna un laberinto de tamaño dimension x dimension con todas las casillas libres
def laberinto_vacio(dimension: int):
    if dimension <= 0:
        return []

    return [
        ['0' for i in range(dimension)] for i in range(dimension)
    ]

# cargar_laberinto retorna el laberinto generado por entrada representado
# como una lista de listas de caracteres: '0', '1', 'I' o 'X'
def cargar_laberinto(entrada: list[str]):
    dimension = len(entrada)
    laberinto = laberinto_vacio(dimension)

    for fila in range(dimension):
        for columna in range(dimension):
            laberinto[fila][columna] = entrada[fila][columna]

    return laberinto

# casilla_fuera_de_rango determina si c está fuera de los bordes de un laberinto de tamaño dim x dim
def casilla_fuera_de_rango(dim: int, c: tuple[int, int]):
    if dim <= 0 or c is None:
        return True

    fila, columna = c
    return fila < 1 or fila > dim or columna < 1 or columna > dim

# casilla_es determina si dentro de lab, la casilla c es tipo,
# donde tipo = '0', '1', 'I' o 'X'
def casilla_es(lab: list[list[str]], c: tuple[int, int], tipo: str):
    if casilla_fuera_de_rango(len(lab), c) or c is None:
        return False

    fila, columna = c
    return lab[fila - 1][columna - 1] == tipo

# obtener_vecinos retorna una lista con las casillas adyacentes a c en dirección norte, este, sur y oeste
# Si los vecinos son válidos o no se chequea luego
def obtener_vecinos(c: tuple[int, int]):
    if c is None:
        return []

    fila, columna = c
    return [(fila - 1, columna), (fila, columna + 1), (fila + 1, columna), (fila, columna - 1)]

# obtener_inicial retorna una tupla (fila, columna) tal que laberinto[fila][columna] == 'I'
# En caso de no encontrar la posicion inicial, retorna None
def obtener_inicial(laberinto: list[list[str]]):
    fila = 0
    columna = 0
    dim = len(laberinto)
    while fila <= dim - 1 and laberinto[fila][columna] != 'I':
        columna += 1
        if columna > dim - 1:
            fila += 1
            columna = 0

    # No hay una posicion inicial
    if fila >= dim:
        return None

    return (fila + 1, columna + 1)

# resolver retorna una manera de llegar desde el punto inicial del lab hasta el objetivo de lab como [(y0, x0), (y1, x1), ..., (yn, xn)]
# Si no se puede llegar de ninguna manera o no hay de dónde empezar, retorna la lista vacía
def resolver(lab: list[list[str]]):
    inicial = obtener_inicial(lab)
    if inicial is None:
        return None

    casillas_a_visitar = [inicial]
    visitadas = set()
    origenes = {}
    c = None

    while not casilla_es(lab, c, 'X') and casillas_a_visitar != []:
        # Nos fijamos en el primer vecino a visitar
        # Esto nos permite chequear distintas direcciones en paralelo
        c = casillas_a_visitar.pop(0)
        visitadas.add(c)
        vecinos = obtener_vecinos(c)
        for vecino in vecinos:
            if not casilla_fuera_de_rango(len(lab), vecino) and vecino not in visitadas \
                and not casilla_es(lab, vecino, '1'):
                    # Marcamos de dónde viene el vecino así luego podemos determinar el camino
                    # en caso de encontrar la casilla objetivo
                    origenes[vecino] = c
                    casillas_a_visitar.append(vecino)

    camino = []
    if casilla_es(lab, c, 'X'):
        # Retrocedemos en los vecinos del objetivo hasta encontrar la posición inicial
        while c != inicial:
            camino.append(c)
            c = origenes[c]

        if c == inicial:
            camino.append(c)
    elif casillas_a_visitar == []:
        # No hay una manera de llegar hasta el objetivo
        return []

    return camino[::-1]

def main():
    if len(sys.argv) < 2:
        print("uso: python", sys.argv[0], "<laberinto generado>")
        return

    f = open(sys.argv[1], "r")
    laberinto = cargar_laberinto(f.readlines())
    if laberinto == []:
        print("No se pudo cargar el laberinto")
        return
    f.close()

    camino = resolver(laberinto)
    if camino == None:
        print("No se encontró el punto inicial")
        return

    # Si no hay una solucion para el laberinto, generamos
    # uno nuevo con las mismas especificaciones
    while camino == []:
        f = open(sys.argv[1], "r")
        subprocess.run(["./a.out", "EntradaLaberinto.txt"])
        laberinto = cargar_laberinto(f.readlines())
        f.close()

        camino = resolver(laberinto, inicial)

    print(camino)

if __name__ == '__main__':
    main()

## -----
## Tests
## -----
def test_laberinto_vacio():
    assert laberinto_vacio(4) == [
        ['0', '0', '0', '0'],
        ['0', '0', '0', '0'],
        ['0', '0', '0', '0'],
        ['0', '0', '0', '0']
    ]

    assert laberinto_vacio(1) == [['0']]
    assert laberinto_vacio(0) == []
    assert laberinto_vacio(-9) == []
    assert laberinto_vacio(9) == [
        ['0', '0', '0', '0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0', '0', '0', '0']
    ]

def test_cargar_laberinto():
    test1 = ["000\n", "010\n", "I1X\n"]
    assert cargar_laberinto(test1) == [
        ['0', '0', '0'],
        ['0', '1', '0'],
        ['I', '1', 'X']
    ]

    test2 = []
    assert cargar_laberinto(test2) == []

    test3 = ["10110X\n", "000001\n", "000101\n", "001111\n", "101001\n", "I00011\n"]
    assert cargar_laberinto(test3) == [
        ['1', '0', '1', '1', '0', 'X'],
        ['0', '0', '0', '0', '0', '1'],
        ['0', '0', '0', '1', '0', '1'],
        ['0', '0', '1', '1', '1', '1'],
        ['1', '0', '1', '0', '0', '1'],
        ['I', '0', '0', '0', '1', '1']
    ]

    test4 = ["I1\n", "0X\n"]
    assert cargar_laberinto(test4) == [
        ['I', '1'],
        ['0', 'X']
    ]

    test5 = ["X\n"]
    assert cargar_laberinto(test5) == [['X']]

def test_casilla_fuera_de_rango():
    assert casilla_fuera_de_rango(5, (3, 5)) == False
    assert casilla_fuera_de_rango(5, (5, 3)) == False
    assert casilla_fuera_de_rango(5, (6, 3)) == True
    assert casilla_fuera_de_rango(5, (3, 6)) == True
    assert casilla_fuera_de_rango(0, (1, 1)) == True
    assert casilla_fuera_de_rango(10, None) == True

def test_casilla_es():
    test1 = [
        ['0', '0', '0', 'I'],
        ['1', '1', '1', '0'],
        ['X', '1', '0', '0'],
        ['0', '0', '0', '1'],
    ]
    assert casilla_es(test1, (1, 1), '0') == True
    assert casilla_es(test1, (3, 1), 'X') == True
    assert casilla_es(test1, (4, 1), '1') == False
    assert casilla_es(test1, (6, 7), 'I') == False

    test2 = [
        ['0', 'I', '1'],
        ['X', '1', '0'],
        ['0', '0', '0']
    ]
    assert casilla_es(test2, (0, 0), '3') == False
    assert casilla_es(test2, (1, 1), '3') == False
    assert casilla_es(test2, (1, 1), '0') == True
    assert casilla_es(test2, (2, 1), 'X') == True
    assert casilla_es(test2, (2, 2), '1') == True
    assert casilla_es(test2, (2, 3), None) == False

    test3 = []
    assert casilla_es(test3, (1, 1), '0') == False
    assert casilla_es(test3, (2, 1), 'X') == False
    assert casilla_es(test3, (2, 5), '5') == False
    assert casilla_es(test3, (9, 3), 'I') == False

    test4 = [['X']]
    assert casilla_es(test4, (1, 1), 'X') == True
    assert casilla_es(test4, (1, 2), '0') == False
    assert casilla_es(test4, (9, 3), '1') == False
    assert casilla_es(test4, None, '1') == False

def test_obtener_vecinos():
    assert obtener_vecinos((4, 3)) == [(3, 3), (4, 4), (5, 3), (4, 2)]
    assert obtener_vecinos((1, 1)) == [(0, 1), (1, 2), (2, 1), (1, 0)]
    assert obtener_vecinos((0, 0)) == [(-1, 0), (0, 1), (1, 0), (0, -1)]
    assert obtener_vecinos(None) == []

def test_obtener_inicial():
    test1 = [
        ['0', '0', '0', 'I'],
        ['1', '1', '1', '0'],
        ['X', '1', '0', '0'],
        ['0', '0', '0', '1'],
    ]
    assert obtener_inicial(test1) == (1, 4)

    test2 = [
        ['0', '1', '0'],
        ['X', '1', 'I'],
        ['0', '0', '0']
    ]
    assert obtener_inicial(test2) == (2, 3)

    test3 = [
        ['1', '0', '1', '1', '0', 'X'],
        ['0', '0', '0', '0', '0', '1'],
        ['0', '0', '0', '1', '0', '1'],
        ['0', '0', '1', '1', '1', '1'],
        ['1', '0', '1', '0', '0', '1'],
        ['I', '0', '0', '0', '1', '1']
    ]
    assert obtener_inicial(test3) == (6, 1)

    test4 = [
        ['0', '0', '0'],
        ['0', '1', '0'],
        ['1', '1', 'X']
    ]
    assert obtener_inicial(test4) == None

def test_resolver():
    test1 = [
        ['1', '0', '1', '1', '0', 'X'],
        ['0', '0', '0', '0', '0', '1'],
        ['0', '0', '0', '1', '0', '1'],
        ['0', '0', '1', '1', '1', '1'],
        ['1', '0', '1', '0', '0', '1'],
        ['I', '0', '0', '0', '1', '1']
    ]
    assert resolver(test1) == [(6, 1), (6, 2), (5, 2), (4, 2), (3, 2), (3, 3), (2, 3), (2, 4), (2, 5), (1, 5), (1, 6)]

    test2 = [
        ['0', '0', '0'],
        ['0', '1', '0'],
        ['I', '1', 'X']
    ]
    assert resolver(test2) == [(3, 1), (2, 1), (1, 1), (1, 2), (1, 3), (2, 3), (3, 3)]

    test3 = [
        ['0', '0', '0', 'I'],
        ['1', '1', '1', '0'],
        ['X', '1', '0', '0'],
        ['0', '0', '0', '1'],
    ]
    assert resolver(test3) == [(1, 4), (2, 4), (3, 4), (3, 3), (4, 3), (4, 2), (4, 1), (3, 1)]

    test4 = [
        ['0', '0', '0', 'I'],
        ['1', '1', '1', '0'],
        ['X', '1', '0', '0'],
        ['1', '0', '0', '1'],
    ]
    assert resolver(test4) == []

    test5 = [
        ['I', '0'],
        ['0', 'X'],
    ]
    assert resolver(test5) == [(1, 1), (2, 1), (2, 2)]

    test6 = [['X']]
    assert resolver(test6) == None

    test7 = [
        ['I', '1', '0', '0', '0', '1'],
        ['0', '1', '0', '1', '0', '1'],
        ['0', '1', '0', '1', '0', '1'],
        ['0', '1', '0', '1', '0', '1'],
        ['0', '1', '0', '1', '0', '1'],
        ['0', '0', '0', '1', '0', 'X']
    ]
    assert resolver(test7) == [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1),
                               (6, 2), (6, 3), (5, 3), (4, 3), (3, 3), (2, 3), (1, 3),
                               (1, 4), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (6, 6)]

    test8 = []
    assert resolver(test8) == None

    test9 = [
        ['I', 'X'],
        ['0', '0']
    ]
    assert resolver(test9) == [(1, 1), (1, 2)]

    test10 = [['I']]
    assert resolver(test10) == []
