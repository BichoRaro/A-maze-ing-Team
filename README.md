# A-Maze-ing

Generador de laberintos en linea de comandos. Lee un fichero de
configuracion, genera un laberinto (perfecto o jugable tipo Pac-Man)
con un patron "42" protegido en el centro, calcula el camino mas
corto entre la entrada y la salida, escribe un fichero de salida y
muestra el resultado en un menu interactivo en la terminal.

## Instalacion

Este proyecto no tiene dependencias de terceros para ejecutarse (solo
usa la libreria estandar de Python). `flake8`, `mypy` y `build` son
herramientas de desarrollo, necesarias para lint, comprobacion de
tipos y para reconstruir el paquete `mazegen`.

```bash
python3 -m venv venv
source venv/bin/activate
make install
```

`make install` instala `requirements.txt` (herramientas de
desarrollo fijadas por version) y, ademas, el propio proyecto en modo
editable con el extra `dev` definido en `pyproject.toml`.

## Uso

```bash
make run                       # usa config.txt por defecto
make run CONFIG=otro.txt       # usa un fichero de configuracion distinto
make debug                     # ejecuta bajo pdb
```

El fichero de configuracion debe definir, como minimo, `WIDTH`,
`HEIGHT`, `ENTRY`, `EXIT`, `OUTPUT_FILE` y `PERFECT`. Ver
`config.txt` para un ejemplo.

## Desarrollo

```bash
make lint           # flake8 + mypy
make lint-strict     # flake8 + mypy --strict
make build           # reconstruye mazegen-1.0.0-py3-none-any.whl y .tar.gz
make clean            # elimina caches, dist/, build/ y *.egg-info
```

## Estructura del repositorio

```
.
├── a_maze_ing.py            # punto de entrada (menu interactivo)
├── maze_analyzer.py         # analizador standalone de ficheros de salida
├── parse_config.py          # lectura y validacion de config.txt
├── output_writer.py         # escritura del fichero de salida
├── display/
│   └── ascii_display.py     # renderizado ASCII en terminal
├── mazegen/                 # modulo reutilizable (ver documentacion abajo)
│   ├── __init__.py
│   ├── generator.py
│   └── README.md
├── mazegen-1.0.0-py3-none-any.whl
├── mazegen-1.0.0.tar.gz
├── pyproject.toml
├── LICENSE.md
└── requirements.txt
```

## El modulo `mazegen`

`mazegen` es un modulo reutilizable e independiente: no depende de
ningun otro fichero de este repositorio y puede instalarse por
separado con pip (`mazegen-1.0.0-py3-none-any.whl`, en la raiz de
este repositorio) para usarse en cualquier otro proyecto. Su
documentacion completa esta en `mazegen/README.md`; aqui se resume lo
esencial.

### Instanciar y usar: ejemplo basico

```python
from mazegen import MazeGenerator

maze = MazeGenerator(
    width=15,
    height=15,
    entry=(0, 0),
    exit_cell=(14, 14),
)

maze.generate()          # laberinto perfecto por defecto (perfect=True)

print(maze.to_hex())     # representacion hexadecimal, una fila por linea
```

### Parametros personalizados (tamano, seed, modo jugable)

```python
maze = MazeGenerator(
    width=21,
    height=21,
    entry=(0, 0),
    exit_cell=(20, 20),
    seed=42,                # opcional: generacion reproducible
)

maze.generate(perfect=False)   # False -> tablero jugable tipo Pac-Man
                                # True (por defecto) -> laberinto perfecto
```

Si no se pasa `seed`, se genera una aleatoria y se guarda en
`maze.seed`. `maze.regenerate()` genera una nueva semilla aleatoria
(hay que volver a llamar a `generate()` despues).

### Acceder a la estructura generada y a una solucion

```python
maze.grid            # estructura interna: lista de filas, cada una
                      # una lista de celdas; cada celda es un dict
                      # {"North": bool, "East": bool, "South": bool,
                      # "West": bool} (True = pared cerrada)

maze.to_hex()          # str: un digito hexadecimal por celda
maze.grid_to_ints()     # list[list[int]]: mismo encoding, como enteros

path_letters = maze.bfs()                       # ['E', 'E', 'S', ...]
path_coords = maze.path_to_coords(path_letters)  # [(0,0), (1,0), ...]
```

`maze.bfs()` calcula el camino mas corto entre `maze.entry` y
`maze.exit_cell` mediante BFS. `maze.path_to_coords()` convierte esa
lista de letras de direccion en la lista de coordenadas `(x, y)`
recorridas.

`mazegen.MazeError` se lanza si la entrada, la salida o la celda de
inicio del DFS caen dentro del patron "42" protegido del centro.

## Licencia

Este repositorio, incluido el modulo `mazegen`, se distribuye bajo la
licencia MIT. Ver `LICENSE.md` para el texto completo y la
justificacion de la eleccion.