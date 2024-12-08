# Resolvedor de laberintos

## Instrucciones
- abrir una consola en la raíz del proyecto
- compilar el programa de C: `gcc -Wall -Werror -Wextra main.c`
- ejecutar el programa de C: `./a.out EntradaLaberinto.txt`
(este programa produce el archivo SalidaLaberinto.txt)
- ejecutar el programa de Python: `python3 main.py SalidaLaberinto.txt`

### Consideraciones
- El programa compilado de C debe llamarse a.out
- La configuración del laberinto debe llamarse EntradaLaberinto.txt
- El programa en Python requiere que exista el programa compilado de C.
- EntradaLaberinto.txt tiene el siguiente formato:
```
dimension
n
obstaculos fijos
(y,x)
(y,x)
...
obstaculos aleatorios
n
posicion inicial
(y,x)
objetivo
(y,x)
```
- El laberinto dado siempre tiene solución.
- Si el laberinto generado no tiene solución, el programa en Python
genera uno nuevo con la misma configuración
(por eso requiere que exista el programa compilado de C).

### Correr tests en Python
```
python -m pytest main.py
```
