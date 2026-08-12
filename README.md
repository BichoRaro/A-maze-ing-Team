# 📁 PROYECTO A-MAZE-ING

## ✅ HECHO

- [x] **parse_config.py** → Parseo del `config.txt`

- [x] **mazegen/generator.py** → Clase `MazeGenerator` completa
  - [x] `__init__()` → Inicialización con width, height, entry, exit, seed
  - [x] `generate(perfect)` → Lanza DFS + patrón 42 + modo imperfecto
  - [x] `_carve()` → Algoritmo DFS con backtracking
  - [x] `_place_42()` → Patrón 42 en el centro
  - [x] `_add_loops()` → Bucles aleatorios (modo Pac-Man)
  - [x] `_make_imperfect()` → Tablero tipo Pac-Man
  - [x] `_open_corners()` → Esquinas abiertas
  - [x] `_open_center()` → Centro abierto
  - [x] `bfs()` → Camino más corto (entrada → salida)
  - [x] `to_hex()` → Exportar laberinto a hexadecimal
  - [x] `grid_to_ints()` → Convertir grid a enteros para el display
  - [x] `path_to_coords()` → Convertir letras a coordenadas

- [x] **mazegen/__init__.py** → Paquete mazegen importable

- [x] **output_writer.py** → Escribe el fichero de salida
  - [x] Hex del laberinto fila por fila
  - [x] Línea vacía
  - [x] Coordenadas de entrada → `x,y`
  - [x] Coordenadas de salida → `x,y`
  - [x] Camino más corto → `NNEESSWW...`

- [x] **a_maze_ing.py** → Punto de entrada principal
  - [x] Lectura de argumentos (`sys.argv`)
  - [x] Llamada a `parse_config()`
  - [x] Creación de `MazeGenerator`
  - [x] Llamada a `generate()`
  - [x] Llamada a `bfs()`
  - [x] Llamada a `write_output()`
  - [x] Llamada a `display.run_menu()`

- [x] **config.txt** → Fichero de configuración por defecto

- [x] **display/ascii_display.py** → Renderizado terminal (parcial)
  - [x] `render()` → Dibuja el laberinto
  - [x] `toggle_path()` → Mostrar/ocultar camino
  - [x] `set_wall_color()` → Cambiar color de paredes
  - [ ] `run_menu()` → **PENDIENTE** (está vacío)

---

## ⬜ POR HACER (Obligatorio)

- [ ] **display/ascii_display.py**
  - [ ] `run_menu()` → Menú interactivo (1-4)

- [ ] **Makefile**
  - [ ] `install`
  - [ ] `run`
  - [ ] `debug`
  - [ ] `clean`
  - [ ] `lint`

- [ ] **LICENSE.md** → Licencia *(obligatorio en v2.2)*

---

## 📦 POR HACER (Empaquetado)

- [ ] **pyproject.toml** → Configuración para construir el paquete pip
- [ ] **mazegen-*.whl** → Paquete instalable

---

## 📚 POR HACER (Documentación)

- [ ] **README.md** → README real del proyecto (descripción, instrucciones, recursos)