# 📁 PROYECTO A-MAZE-ING

## ✅ HECHO

- [x] **parse_config.py**
  - Parseo del `config.txt`

- [x] **generator.py**
  - [x] `__init__()`
  - [x] `generate()` *(falta conectar `_place_42()` y `_make_imperfect()`)*
  - [x] `_carve()` → DFS Backtracking
  - [x] `_place_42()` → Patrón 42
  - [x] `_make_imperfect()` → Necesita mejoras (Pac-Man rules)
  - [x] `bfs()` → Camino más corto
  - [x] `to_hex()` → Exportar a hexadecimal

- [x] **generator.py**
  - [x] `generate()`
    - Conectar `_place_42()`
    - Conectar `_make_imperfect()`

---

## ⬜ POR HACER (Obligatorio)

- [ ] **output_writer.py**
  - [ ] Escribir el fichero de salida
    - Hex del laberinto (fila por fila)
    - Línea vacía
    - Coordenadas de entrada → `1,1  # entry (x,y)`
    - Coordenadas de salida → `19,14  # exit (x,y)`
    - Camino más corto → `NNEESSWW...`

- [ ] **display/ascii_display.py**
  - [ ] Renderizado en terminal
    - Dibujar paredes
    - Marcar entrada y salida
    - Mostrar camino más corto (toggle)
    - Cambiar colores de paredes
    - Menú interactivo (1-4)

- [ ] **a_maze_ing.py**
  - [ ] Punto de entrada (`main`)
    - Leer `sys.argv[1]` → Config file
    - Llamar `parse_config()`
    - Crear `MazeGenerator`
    - Llamar `generate()`
    - Llamar `bfs()`
    - Llamar `output_writer()`
    - Llamar `ascii_display()`

- [ ] **Makefile**
  - `install`
  - `run`
  - `debug`
  - `clean`
  - `lint`

- [ ] **config.txt**
  - Fichero de configuración por defecto

- [ ] **LICENSE.md**
  - Licencia *(nuevo en v2.2)* ⚠️

---

## 📦 POR HACER (Empaquetado)

- [ ] **pyproject.toml**
  - Configuración para construir el paquete `pip`

- [ ] **mazegen-*.whl**
  - Paquete instalable

---

## 📚 POR HACER (Documentación)

- [ ] **README.md**
  - Descripción del proyecto
  - Instrucciones de instalación
  - Uso
  - Recursos
  - Ejemplos