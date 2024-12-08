#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define TAM_LINEA 1024

typedef struct Laberinto {
    char **tablero;
    int dimension;
    int n_obstaculos;
} Laberinto;

typedef struct Punto {
    int y;
    int x;
} Punto;

/* Utils */

int leer_int(char *, int *);
int leer_punto(char *, Punto *);
char *avanzar_linea(FILE *, char *);

/* Laberinto */

void alocar_laberinto(Laberinto *);
void liberar_laberinto(Laberinto *);
void ubicar_en(Laberinto *, Punto, char);
int casilla_ocupada(Laberinto *, Punto);

/* Cargar y escribir */

void leer_dimension(Laberinto *, char *, FILE *);
void ubicar_obstaculos(Laberinto *, char *, FILE *);
void leer_obstaculos_aleatorios(Laberinto *, char *, FILE *);
void ubicar_inicial(Laberinto *, char *, FILE *);
void ubicar_objetivo(Laberinto *, char *, FILE *);
void ubicar_obstaculos_aleatorios(Laberinto *);
void cargar_laberinto(Laberinto *, const char *);
void escribir_laberinto(Laberinto *);

int main(int argc, char **argv)
{
    if (argc < 2) {
        printf("uso: %s <configuracion>\n", argv[0]);
        return 1;
    }

    srand(time(NULL));

    Laberinto lab;
    cargar_laberinto(&lab, argv[1]);
    escribir_laberinto(&lab);

    liberar_laberinto(&lab);
    return 0;
}

/* Utils */

// leer_int lee el valor de un int x desde un string s
// Retorna cuántos enteros leyó correctamente
int leer_int(char *s, int *x)
{
    return sscanf(s, "%d", x);
}

// leer_punto lee un par de enteros a una estructura Punto p desde un string s
// Retorna cuántos enteros leyó correctamente
int leer_punto(char *s, Punto *p)
{
    return sscanf(s, "(%d,%d)", &p->y, &p->x);
}

// avanzar_linea lee la siguiente linea del archivo f y guarda el contenido en linea
// Retorna un puntero al contenido guardado en linea
char *avanzar_linea(FILE *f, char *linea)
{
    return fgets(linea, TAM_LINEA, f);
}

/* Laberinto */

// alocar_laberinto aloca suficiente memoria para la representacion del laberinto
// e inicializa cada valor con el caracter '0'
void alocar_laberinto(Laberinto *lab)
{
    lab->tablero = malloc(lab->dimension * sizeof(char *));
    assert(lab->tablero != NULL);
    for (int i = 0; i < lab->dimension; ++i) {
        lab->tablero[i] = malloc(lab->dimension * sizeof(char));
        assert(lab->tablero[i] != NULL);
    }

    for (int fila = 1; fila <= lab->dimension; ++fila) {
        for (int columna = 1; columna <= lab->dimension; ++columna) {
            Punto p = { fila, columna };
            ubicar_en(lab, p, '0');
        }
    }
}

// liberar_laberinto libera de la memoria un laberinto alocado por alocar_laberinto
void liberar_laberinto(Laberinto *lab)
{
    for (int i = 0; i < lab->dimension; ++i)
        free(lab->tablero[i]);

    free(lab->tablero);
}

// ubicar_en ubica tipo_casilla en el punto p(y, x) de lab
void ubicar_en(Laberinto *lab, Punto p, char tipo_casilla)
{
    int tipo_casilla_invalido = tipo_casilla != '0' && tipo_casilla != '1' &&
                              tipo_casilla != 'I' && tipo_casilla != 'X';
    if (tipo_casilla_invalido || p.x < 1 || p.x > lab->dimension || p.y < 1 || p.y > lab->dimension) {
        printf("No se pudo ubicar '%c' en el punto (%d,%d)\n", tipo_casilla, p.y, p.x);
        return;
    }

    lab->tablero[p.y - 1][p.x - 1] = tipo_casilla;
}

// casilla_ocupada determina si la casilla en p(y, x) no está libre
int casilla_ocupada(Laberinto *lab, Punto p)
{
    if (p.x < 1 || p.x > lab->dimension || p.y < 1 || p.y > lab->dimension)
        return 0;

    return lab->tablero[p.y - 1][p.x - 1] != '0';
}

/* Cargar y escribir */

// leer_dimension lee la dimension desde f y la guarda en lab->dimension
void leer_dimension(Laberinto *lab, char *linea, FILE *f)
{
    linea = avanzar_linea(f, linea);
    leer_int(linea, &lab->dimension);

    linea = avanzar_linea(f, linea);
}

// ubicar_obstaculos lee cada obstaculo fijo y los ubica en su respectiva posicion (y, x) dentro de lab
void ubicar_obstaculos(Laberinto *lab, char *linea, FILE *f)
{
    linea = avanzar_linea(f, linea);
    Punto p;
    int salir = 0;
    while (!salir) {
        int n = leer_punto(linea, &p);
        if (n == 2) {
            ubicar_en(lab, p, '1');
            linea = avanzar_linea(f, linea);
        } else
            salir = 1;
    }
}

// leer_obstaculos_aleatorios lee la cantidad de obstaculos aleatorios desde el archivo de entrada
// y guarda el resultado en lab->n_obstaculos
void leer_obstaculos_aleatorios(Laberinto *lab, char *linea, FILE *f)
{
    linea = avanzar_linea(f, linea);
    leer_int(linea, &lab->n_obstaculos);
    linea = avanzar_linea(f, linea);
}

// ubicar_inicial lee el punto de la sección "posicion inicial" desde el archivo de entrada
// y lo ubica en el laberinto
void ubicar_inicial(Laberinto *lab, char *linea, FILE *f)
{
    linea = avanzar_linea(f, linea);
    Punto p;
    leer_punto(linea, &p);

    ubicar_en(lab, p, 'I');
    linea = avanzar_linea(f, linea);
}

// ubicar_objetivo lee el punto de la sección "objetivo" desde el archivo de entrada
// y lo ubica en el laberinto
void ubicar_objetivo(Laberinto *lab, char *linea, FILE *f)
{
    linea = avanzar_linea(f, linea);
    Punto p;
    leer_punto(linea, &p);

    ubicar_en(lab, p, 'X');
    linea = avanzar_linea(f, linea);
}

// ubicar_obstaculos_aleatorios genera y ubica lab->n_obstaculos puntos aleatorios dentro del laberinto
// Si un punto generado cae sobre algo que ya existe en el laberinto, lo genera hasta que no sea el caso
void ubicar_obstaculos_aleatorios(Laberinto *lab)
{
    for (int i = 0; i < lab->n_obstaculos; ++i) {
        Punto p = {
            (rand()%lab->dimension) + 1,
            (rand()%lab->dimension) + 1,
        };

        // No podemos ubicar obstáculos donde ya los hay
        while (casilla_ocupada(lab, p)) {
            p.x = (rand()%lab->dimension) + 1;
            p.y = (rand()%lab->dimension) + 1;
        }

        ubicar_en(lab, p, '1');
    }
}

// cargar_laberinto escribe los datos dados por el archivo de entrada a lab
void cargar_laberinto(Laberinto *lab, const char *entrada)
{
    FILE *f = fopen(entrada, "r");
    if (f == NULL) {
        printf("error: El archivo '%s' no pudo ser cargado\n", entrada);
        return;
    }

    char linea[TAM_LINEA] = { 0 };

    // Se asume que el formato es correcto con información que
    // va a generar un laberinto válido
    avanzar_linea(f, linea);

    leer_dimension(lab, linea, f);
    alocar_laberinto(lab);
    ubicar_obstaculos(lab, linea, f);
    leer_obstaculos_aleatorios(lab, linea, f);
    ubicar_inicial(lab, linea, f);
    ubicar_objetivo(lab, linea, f);
    ubicar_obstaculos_aleatorios(lab);

    fclose(f);
}

// escribir_laberinto escribe en un archivo la representacion gráfica de lab
void escribir_laberinto(Laberinto *lab)
{
    FILE *f = fopen("SalidaLaberinto.txt", "w");
    for (int y = 0; y < lab->dimension; ++y) {
        for (int x = 0; x < lab->dimension; ++x) {
            fprintf(f, "%c", lab->tablero[y][x]);
        }
        fprintf(f, "\n");
    }

    fclose(f);
}
