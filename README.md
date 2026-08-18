# A-Maze-ing

**Este proyecto ha sido realizado como parte del programa educativo de 42 [aykhan-i] y [oduran-m]*

## Descripción

A-Maze-ing es una herramienta basada en Python para la generación y visualización de laberintos. El objetivo de este proyecto es implementar un sistema robusto capaz de generar laberintos aleatorios “perfectos” o “imperfectos” a partir de un archivo de configuración, resolverlos mediante algoritmos de teoría de grafos y proporcionar una interfaz visual interactiva.

El proyecto hace especial énfasis en:

* Pensamiento computacional: Implementación de los algoritmos DFS y BFS.
* Reutilización del código: Creación de un paquete independiente e instalable mediante pip (mazegen).
* Buenas prácticas: Cumplimiento estricto de PEP 8 (flake8), uso de anotaciones de tipos (mypy) y gestión adecuada de errores.

## Instrucciones

### Prerrequisitos
Antes de ejecutar A-Maze-ing, asegúrate de tener instalado:

* Python 3.10
* pip o uv para la gestión del entorno y las dependencias
* flake8 para comprobar el cumplimiento de PEP 8
* mypy para la comprobación de tipos

### Entorno virtual
Se recomienda utilizar un entorno virtual para mantener las dependencias del proyecto aisladas.

1. Crear un entorno virtual
* python3 -m venv venv

2. Activar el entorno virtual
* source venv/bin/activate

### Ejecución 
Para ejecutar el programa usamos el siguente comando:

*python3 a_maze_ing.py config.txt*

## Recursos

* DfS y BFS Visualizador: https://visualgo.net/en

* IA usadas para el proyecto:
    * Gemini
    * Chatgpt
    * Claude

* Depth-First Search (DFS): https://www.datacamp.com/es/tutorial/depth-first-search-in-python

* Solve whith BFS: https://adrian-sebuliba.medium.com/breadth-first-search-bfs-algorithm-dd91cc5506e4

## Estructura y formato del archivo de configuración

El programa recibe como único argumento la ruta a un fichero de configuración en texto plano, con formato `CLAVE=VALOR`, una entrada por línea. Las líneas vacías y las que empiezan por `#` se ignoran, lo que permite comentar el fichero.

Ejemplo de `config.txt`:

```
# Configuración del laberinto
WIDTH=21
HEIGHT=15
ENTRY=0,0
EXIT=20,14
PERFECT=true
OUTPUT_FILE=maze.txt
SEED=42
ALGORITHM=iterative
```

| Clave         | Obligatoria | Tipo               | Descripción                                                                 |
|---------------|:-----------:|---------------------|-------------------------------------------------------------------------------|
| `WIDTH`       | Sí          | entero > 0           | Ancho del laberinto, en número de celdas.                                    |
| `HEIGHT`      | Sí          | entero > 0           | Alto del laberinto, en número de celdas.                                     |
| `ENTRY`       | Sí          | `x,y`                | Coordenada de la celda de entrada (0-indexada, dentro de los límites).       |
| `EXIT`        | Sí          | `x,y`                | Coordenada de la celda de salida. Debe ser distinta de `ENTRY`.              |
| `PERFECT`     | Sí          | booleano             | `true`/`false` (también acepta `1`/`0`, `yes`/`no`). Ver más abajo.          |
| `OUTPUT_FILE` | Sí          | nombre de fichero    | Nombre simple del fichero de salida (sin rutas, ni `.` ni `..`).             |
| `SEED`        | No          | entero               | Semilla para la generación aleatoria. Si se omite, se genera una al azar.    |
| `ALGORITHM`   | No          | `iterative`/`recursive` | Algoritmo de generación. Por defecto `iterative`.                        |

**`PERFECT`** controla el tipo de laberinto generado:
- `true`: laberinto **perfecto**, es decir, un árbol de expansión donde existe exactamente un camino entre cada par de celdas (sin ciclos, sin celdas inaccesibles).
- `false`: tras generar el laberinto perfecto, se aplican pasos adicionales (`_make_imperfect`) que abren paredes extra para crear bucles, reduciendo los callejones sin salida y abriendo las esquinas y el centro — dando como resultado un tablero más abierto, estilo Pac-Man, apto para juego.

El fichero de salida (`OUTPUT_FILE`) generado por `write_output` tiene el siguiente formato, en este orden:

```
<laberinto en hexadecimal, una línea por fila>

<x_entry>,<y_entry>
<x_exit>,<y_exit>
<camino más corto como cadena de letras N/E/S/W>
```

Cada celda del laberinto se codifica como un único dígito hexadecimal que resulta de sumar los valores de sus paredes cerradas: Norte=1, Este=2, Sur=4, Oeste=8. Por ejemplo, una celda con las paredes Norte y Oeste cerradas (y Este/Sur abiertas) se codifica como `1+8=9`.

## Validación de la configuración y manejo de errores

La lectura y validación del fichero de configuración se realiza en `parse_config.py`, dividida en tres fases claramente separadas, cada una con su propia responsabilidad:

1. **`read_config`** — lectura en bruto del fichero. Parsea cada línea `CLAVE=VALOR`, ignorando comentarios y líneas vacías. En esta fase ya se detectan errores de sintaxis: líneas sin `=`, claves o valores vacíos, y claves duplicadas.
2. **`validate_keys`** — comprueba que están presentes todas las claves obligatorias (`WIDTH`, `HEIGHT`, `ENTRY`, `EXIT`, `OUTPUT_FILE`, `PERFECT`) antes de intentar convertir ningún valor.
3. **`typing_validating`** — convierte cada valor de texto a su tipo real (enteros, tuplas de coordenadas, booleano) y aplica las reglas de negocio: `WIDTH`/`HEIGHT` deben ser positivos, `ENTRY` y `EXIT` deben caer dentro de los límites del laberinto y no pueden coincidir, `OUTPUT_FILE` debe ser un nombre de fichero simple (sin `/`, ni `.`/`..`), y `ALGORITHM` debe ser uno de los valores permitidos.

Todos los errores de esta cadena —de sintaxis, de claves ausentes o de valores inválidos— se comunican mediante una única excepción personalizada, `ConfigError`, con un mensaje descriptivo del problema concreto. Esto permite que `main()` capture un solo tipo de excepción y muestre un mensaje claro al usuario sin necesidad de inspeccionar múltiples tipos de error:

```python
except ConfigError as exc:
    print(f"Configuration error: {exc}")
    return
```

Aparte, el propio proceso de generación puede fallar con `MazeError` (por ejemplo, si `ENTRY` o `EXIT` caen dentro del patrón "42" protegido), y las operaciones de escritura de fichero pueden lanzar `OSError`. Cada una se captura por separado en su punto correspondiente (`build_maze`, `run_menu`), de modo que un fallo nunca deja el programa en un estado inconsistente ni interrumpe el bucle del menú salvo cuando es estrictamente necesario.

## Algoritmo de generación del laberinto

El laberinto se genera con **búsqueda en profundidad (DFS) iterativa**, implementada con una pila explícita en `MazeGenerator._carve`, siguiendo el enfoque clásico de "recursive backtracker":

1. Se parte de la celda de entrada, marcada como visitada, y se apila.
2. En cada iteración se mira la celda en la cima de la pila y se baraja aleatoriamente el orden de las cuatro direcciones (Norte, Este, Sur, Oeste) usando el generador `random.Random(seed)` propio de la instancia.
3. Si alguna dirección lleva a una celda vecina válida (dentro de límites, no visitada y fuera del patrón "42"), se derriba la pared entre ambas celdas, se marca la vecina como visitada y se apila, avanzando el DFS.
4. Si ninguna dirección es válida (callejón sin salida), se hace *backtrack* desapilando la celda actual.
5. El proceso termina cuando la pila queda vacía, momento en el que todas las celdas accesibles han sido visitadas y el laberinto queda completamente conectado.

Antes de lanzar el DFS, `_place_42` reserva un conjunto de celdas en el centro del laberinto dibujando el patrón "42" del proyecto, y `_protect_42` cierra todas sus paredes (incluidas las de las celdas vecinas que dan hacia el patrón), de modo que el DFS nunca entra en esa zona ni la atraviesa.

Si `PERFECT=false`, tras el DFS se ejecuta `_make_imperfect`, que aplica tres pasos adicionales sobre el árbol ya generado:
- **`_braid`**: recorre los callejones sin salida y derriba paredes hacia vecinos cerrados hasta dejar como máximo 2, introduciendo bucles controlados.
- **`_open_corners`**: garantiza que las cuatro esquinas tengan al menos una conexión abierta.
- **`_open_center`**: garantiza que la celda central tenga al menos una conexión abierta.

Una vez generado el laberinto, `MazeGenerator.bfs` calcula el camino más corto entre `ENTRY` y `EXIT` mediante **búsqueda en anchura (BFS)** con `collections.deque`, reconstruyendo el camino a partir de un diccionario `came_from` y devolviéndolo como una secuencia de letras `N`/`E`/`S`/`W`.

**¿Por qué DFS iterativo para la generación y BFS para la resolución?**
- El DFS con backtracking genera laberintos **perfectos** por construcción (un único camino entre cualquier par de celdas), que es el requisito base del proyecto, sin necesidad de una fase de post-procesado para eliminar ciclos.
- Al implementarse de forma **iterativa con una pila** en vez de recursiva, se evita el riesgo de alcanzar el límite de recursión de Python en laberintos grandes.
- El resultado tiene una textura característica de pasillos largos y sinuosos con pocas bifurcaciones, típica del recursive backtracker, visualmente reconocible.
- Al depender de un único `random.Random(seed)`, la generación es **determinista y reproducible**: la misma semilla siempre produce el mismo laberinto.
- El BFS es la elección natural para el camino más corto porque, al explorar por niveles, garantiza encontrar el camino de menor número de pasos en un grafo no ponderado como el de las celdas del laberinto — algo que un DFS no puede garantizar.
- Ambos algoritmos son clásicos de teoría de grafos, bien documentados y con complejidad O(V + E), lo que los hace robustos incluso en laberintos grandes.

## Reutilización del código

El proyecto está organizado en módulos con responsabilidades claramente separadas, empaquetado además como paquete instalable (`mazegen`), lo que facilita reutilizar partes del código en otros contextos:

- **`mazegen/generator.py` (`MazeGenerator`)** es completamente independiente de la interfaz de usuario y de la entrada/salida por fichero. Recibe únicamente `width`, `height`, `entry`, `exit_cell` y `seed`, y expone una API basada en datos puros (listas, tuplas, diccionarios) — `generate()`, `bfs()`, `to_hex()`, `grid_to_ints()`, `path_to_coords()`. Al estar empaquetado con `mazegen/__init__.py` e instalable vía pip, puede importarse directamente en cualquier otro proyecto (`from mazegen import MazeGenerator`) sin arrastrar dependencias de consola ni de ficheros de configuración.
- **`display/ascii_display.py` (`AsciiDisplay`)** solo depende de una cuadrícula de enteros y de un conjunto de coordenadas — no conoce nada sobre `MazeGenerator` ni sobre cómo se generó el laberinto. Cualquier estructura que produzca una cuadrícula con esa misma codificación de bits (Norte=1, Este=2, Sur=4, Oeste=8) puede reutilizar este renderizador tal cual, incluso un laberinto generado por otro algoritmo distinto al DFS.
- **`parse_config.py`** separa la lectura en bruto (`read_config`), la validación de claves (`validate_keys`) y el tipado/validación de valores (`typing_validating`, `parse_coordinates`, `parse_bool`, `validate_output_file`) en funciones pequeñas e independientes entre sí. Cada una puede reutilizarse por separado — por ejemplo, `parse_coordinates` y `parse_bool` sirven como utilidades genéricas de parseo para cualquier fichero de configuración similar, no solo para este proyecto.
- **`output_writer.py` (`write_output`)** es una función pura sin estado que solo depende de sus parámetros de entrada, lo que la hace trivialmente reutilizable o sustituible por otro formato de salida sin tocar el resto del programa.
- La codificación de paredes en bits (`walls = {'North': 1, 'East': 2, 'South': 4, 'West': 8}`) se usa de forma consistente en `to_hex()`, `grid_to_ints()` y en todo `AsciiDisplay`, actuando como un pequeño "contrato" de formato entre módulos que permite intercambiar la fuente del laberinto (generador, fichero, editor manual) sin cambiar el resto del pipeline.

Esta separación entre generación, validación de configuración, persistencia y visualización sigue el principio de responsabilidad única: cada módulo se puede probar, sustituir o reutilizar de forma aislada, y el cumplimiento estricto de PEP 8 (flake8) y de anotaciones de tipos (mypy) refuerza que esa reutilización sea segura.

## Funcionalidades avanzadas

- **Patrón "42" protegido**: el laberinto incluye el número "42" dibujado en celdas completamente aisladas en su centro (`_place_42` / `_protect_42`), de forma que nunca forma parte del recorrido generado ni del camino más corto.
- **Modo imperfecto tipo Pac-Man** (`PERFECT=false`): convierte el árbol perfecto en un tablero con bucles, sin callejones sin salida excesivos y con las esquinas y el centro siempre accesibles.
- **Cálculo del camino más corto**: mediante BFS (`MazeGenerator.bfs`), que puede mostrarse u ocultarse dinámicamente desde el menú interactivo.
- **Visualización ASCII coloreada en terminal**: renderizado con caracteres de dibujo de cajas (`─│┌┐└┘┬┴┤├┼`) y colores ANSI, con resaltado diferenciado para la entrada, la salida, el patrón "42" y el camino más corto, y rotación de color de las paredes en caliente.
- **Semillas reproducibles**: cada laberinto queda asociado a una semilla (`SEED` en la configuración o generada aleatoriamente), visible en el menú, que permite reproducir exactamente el mismo laberinto.

## Equipo y gestión del proyecto

### Roles

- **aykhan-i**
    * Clase `MazeGenerator` y su inicialización (`mazegen/generator.py`, `mazegen/__init__.py`)
    * `Makefile`
    * `README.md`
    * `output_writer.py`
    * Manejo de errores (`ConfigError`, `MazeError`, `OSError`) en todo el proyecto

- **oduran-m**
    * Definición y validación de la configuración
    * `display/ascii_display.py` (visualización ASCII)
    * `a_maze_ing.py` (punto de entrada, menú interactivo)
    * `parse_config.py`

El reparto siguió, en líneas generales, una división entre la **lógica de generación y persistencia** (aykhan-i: generación del laberinto, escritura de salida, parsing y validación de configuración, manejo de errores) y la **capa de presentación e integración** (oduran-m: visualización ASCII en terminal y el flujo principal del programa que conecta configuración, generación y menú), lo que permitió a cada miembro avanzar en paralelo sobre módulos con poco acoplamiento entre sí.

### Planificación

Al inicio del proyecto se dividió el trabajo siguiendo la propia arquitectura modular del proyecto: por un lado la generación del laberinto, la persistencia en fichero y la validación de la configuración (`mazegen`, `parse_config.py`, `output_writer.py`), y por otro la visualización y el punto de entrada del programa (`ascii_display.py`, `a_maze_ing.py`). Esta separación permitió trabajar de forma simultánea sin bloquearse mutuamente, siempre que se respetara el "contrato" de datos entre módulos (la cuadrícula de enteros con la codificación de paredes en bits, y el diccionario de configuración tipado devuelto por `parse_config`).

A medida que avanzó el proyecto, la planificación se ajustó para incorporar el manejo de errores de forma centralizada (`ConfigError`, `MazeError`) una vez que ambas partes del proyecto empezaron a integrarse, así como iteraciones adicionales sobre la validación de la configuración y sobre el renderizado ASCII para pulir casos límite que no se habían previsto en el diseño inicial (por ejemplo, la protección completa del patrón "42" frente al DFS, o el braiding de callejones sin salida para el modo imperfecto).

### Qué funcionó bien y qué se podría mejorar

**Funcionó bien:**
- La separación clara de responsabilidades por módulo permitió trabajar en paralelo con muy pocos conflictos de integración.
- Definir pronto el formato de datos compartido entre módulos (la codificación de paredes en bits y la estructura del diccionario de configuración) facilitó que la generación, la validación y la visualización encajaran sin apenas fricción al integrarlas.
- El uso de excepciones personalizadas (`ConfigError`, `MazeError`) permitió centralizar y estandarizar el manejo de errores en todo el proyecto.

**Se podría mejorar:**
- Anticipar antes los casos límite de la configuración y de la generación (coordenadas dentro del patrón "42", laberintos muy pequeños, etc.), en lugar de irlos detectando durante la integración.
- Reforzar la cobertura de tests automatizados desde el principio, en lugar de validar principalmente de forma manual.
- Documentar antes el contrato de datos entre módulos (formato exacto de la cuadrícula, claves del diccionario de configuración) para reducir el tiempo de ajuste al integrar las dos partes del proyecto.

### Herramientas utilizadas

- **flake8** para comprobar el cumplimiento de PEP 8.
- **mypy** para la comprobación de tipos.
- **pip / uv** para la gestión del entorno y las dependencias.
- **Git / GitHub** para el control de versiones y la colaboración entre ambos miembros del equipo.
- **Gemini, ChatGPT y Claude** como apoyo de IA durante el desarrollo (ver sección "Recursos").