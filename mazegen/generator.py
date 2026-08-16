"""Maze generation module — MazeGenerator class."""
import random
from typing import List, Optional, Tuple, Dict
from collections import deque


class MazeError(Exception):
    """
    Clase creada para manejar los excepciones del objeto maze.
    """
    pass


class MazeGenerator:

    # Valor de cada pared como bit (se suman para formar el hexadecimal)
    walls: Dict[str, int] = {
        'North': 1,
        'East': 2,
        'South': 4,
        'West': 8
    }

    # Para cada dirección, su dirección contraria
    # (necesario para derribar paredes en las DOS celdas a la vez)
    opposite_move: Dict[str, str] = {'North': 'South', 'East': 'West',
                                     'South': 'North', 'West': 'East'}

    # Desplazamiento (dx, dy) para moverse en cada dirección
    # North sube (y-1), South baja (y+1), East derecha (x+1), West izquierda
    # (x-1)
    Move: Dict[str, Tuple[int, int]] = {
        'North': (0, -1), 'East': (1, 0), 'South': (0, 1), 'West': (-1, 0)
    }

    def __init__(self,
                 width: int,
                 height: int,
                 entry: Tuple[int, int],
                 exit_cell: tuple[int, int],
                 seed: Optional[int] = None) -> None:
        """Inicializa el generador con el tamaño, entrada, salida y semilla."""

        self.pattern_42_cells: List[Tuple[int, int]] = []
        # Tamaño del laberinto
        self.width = width
        self.height = height

        # Coordenadas de entrada y salida
        self.entry = entry
        self.exit_cell = exit_cell

        # Si no se pasa seed, generamos una aleatoria para reproducibilidad
        if seed is None:
            seed = random.randint(0, 1_000_000)

        # Guardamos la seed real usada (puede ser la generada arriba)
        self.seed = seed

        # Generador aleatorio AISLADO: no interfiere con otros
        # random del programa
        self.rng = random.Random(seed)

        # Grid de celdas (se rellena en generate())
        self.grid: List[List[dict[str, bool]]] = []

        # Registro de celdas visitadas durante el DFS
        # (se rellena en generate())
        self.visited: List[List[bool]] = []

    def regenerate(self) -> None:
        """Genera una nueva seed aleatoria y resetea el rng."""
        self.seed = random.randint(0, 1_000_000)
        self.rng = random.Random(self.seed)

    def generate(self, perfect: bool = True) -> None:
        """Prepara el grid con todas las paredes cerradas y lanza el DFS."""

        # Todas las celdas empiezan con las 4 paredes cerradas (True)
        self.grid = [
            [{"North": True, "East": True, "South": True, "West": True}
                for _ in range(self.width)]
            for _ in range(self.height)
        ]

        # Todas las celdas empiezan sin visitar
        self.visited = [
            [False for _ in range(self.width)]
            for _ in range(self.height)
        ]
        self._place_42()
        self._protect_42()
        entry_x, entry_y = self.entry
        self._carve(entry_x, entry_y)
        if not perfect:
            self._make_imperfect()

    def _carve(self, x: int, y: int) -> None:
        """Genera el laberinto mediante DFS iterativo."""

        # La entrada nunca debe estar dentro del patrón 42
        if (x, y) in self.pattern_42_cells:
            raise MazeError("ENTRY cannot be inside the 42 pattern")

        # Pila explícita para evitar recursión
        stack = [(x, y)]

        # Marcamos la celda inicial como visitada
        self.visited[y][x] = True

        while stack:
            # Celda actual
            cx, cy = stack[-1]

            # Direcciones aleatorias
            directions = ['North', 'East', 'South', 'West']
            self.rng.shuffle(directions)

            # Buscamos una vecina válida
            moved = False

            for direction in directions:
                dx, dy = self.Move[direction]
                nx = cx + dx
                ny = cy + dy

                # La vecina debe:
                # 1. Estar dentro del grid
                # 2. No pertenecer al patrón 42
                # 3. No haber sido visitada
                if (0 <= nx < self.width
                        and 0 <= ny < self.height
                        and (nx, ny) not in self.pattern_42_cells
                        and not self.visited[ny][nx]):

                    # Derribamos la pared en ambas celdas
                    opposite = self.opposite_move[direction]

                    self.grid[cy][cx][direction] = False
                    self.grid[ny][nx][opposite] = False

                    # Marcamos la vecina como visitada
                    self.visited[ny][nx] = True

                    # Continuamos el DFS desde la nueva celda
                    stack.append((nx, ny))

                    moved = True
                    break

            # No hay vecinos válidos → backtracking
            if not moved:
                stack.pop()

    def _place_42(self) -> None:
        """Dibuja el número 42 en el centro del laberinto
        usando celdas con todas las paredes cerradas."""

        self.pattern_42_cells = []

        pattern_4 = [
            (0, 0),
            (0, 1),
            (0, 2), (1, 2), (2, 2),
                            (2, 3),
                            (2, 4),
        ]
        pattern_2 = [
            (4, 0), (5, 0), (6, 0),
                            (6, 1),
            (4, 2), (5, 2), (6, 2),
            (4, 3),
            (4, 4), (5, 4), (6, 4),
        ]

        x0 = self.width // 2 - 3
        y0 = self.height // 2 - 2

        full_pattern = pattern_4 + pattern_2

        # Calcular todas las celdas reales del patrón
        cells = [
            (x0 + dx, y0 + dy)
            for dx, dy in full_pattern
            if 0 <= x0 + dx < self.width and 0 <= y0 + dy < self.height
        ]

        # Dibujar el patrón
        for x_real, y_real in cells:
            self.grid[y_real][x_real] = {
                "North": True,
                "East": True,
                "South": True,
                "West": True
            }
            self.visited[y_real][x_real] = True
            self.pattern_42_cells.append((x_real, y_real))

    def _protect_42(self) -> None:
        """Asegura que el patrón 42 queda completamente aislado."""

        for x, y in self.pattern_42_cells:
            # Las cuatro paredes de la celda del 42 quedan cerradas
            for direction in self.Move:
                self.grid[y][x][direction] = True

            # Cerramos también la conexión desde cualquier vecino
            # que pueda apuntar hacia esta celda del 42
            for direction, (dx, dy) in self.Move.items():
                nx = x + dx
                ny = y + dy

                if (0 <= nx < self.width
                        and 0 <= ny < self.height):
                    opposite = self.opposite_move[direction]
                    self.grid[ny][nx][opposite] = True

    def _braid(self, max_dead_ends: int = 2) -> None:
        """Elimina dead-ends derribando paredes hasta que queden
        como máximo max_dead_ends callejones sin salida."""

        def is_dead_end(x: int, y: int) -> bool:
            """Una celda es dead-end si solo tiene 1 pared abierta."""
            cell = self.grid[y][x]
            open_walls = sum(1 for v in cell.values() if v is False)
            return open_walls == 1

        def get_closed_neighbors(x: int, y: int) -> List[Tuple[str, int, int]]:
            """Devuelve vecinos accesibles con pared cerrada entre ellos."""
            neighbors = []
            for direction, (dx, dy) in self.Move.items():
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.width
                        and 0 <= ny < self.height
                        and self.grid[y][x][direction] is True
                        and (nx, ny) not in self.pattern_42_cells):
                    neighbors.append((direction, nx, ny))
            return neighbors

        # Bucle principal: seguir hasta que queden <= max_dead_ends
        while True:
            # Encontrar todos los dead-ends actuales
            dead_ends = [
                (x, y)
                for y in range(self.height)
                for x in range(self.width)
                if (x, y) not in self.pattern_42_cells
                and is_dead_end(x, y)
            ]

            # Si ya tenemos pocos dead-ends, paramos
            if len(dead_ends) <= max_dead_ends:
                break

            # Mezclar para aleatoriedad
            self.rng.shuffle(dead_ends)

            # Eliminar cada dead-end derribando una pared
            for x, y in dead_ends:
                if not is_dead_end(x, y):
                    continue  # puede que ya no sea dead-end

                neighbors = get_closed_neighbors(x, y)
                if not neighbors:
                    continue  # no hay vecinos disponibles

                # Elegir un vecino al azar y derribar la pared
                direction, nx, ny = self.rng.choice(neighbors)
                opposite = self.opposite_move[direction]
                self.grid[y][x][direction] = False
                self.grid[ny][nx][opposite] = False

    def _make_imperfect(self, probability: float = 0.3) -> None:
        """Convierte el laberinto en un tablero tipo Pac-Man."""

        # Paso 1: crear bucles derribando paredes extra aleatoriamente
        self._braid()

        # Paso 2: garantizar que las 4 esquinas tienen al menos una salida
        self._open_corners()

        # Paso 3: garantizar que el centro tiene al menos una salida
        self._open_center()

    def _open_corners(self) -> None:
        """Asegura que las 4 esquinas tienen al menos una conexión abierta."""

        # Definimos las 4 esquinas con sus dos paredes internas posibles
        # Formato: (x, y, primera_pared_interna, segunda_pared_interna)
        corners = [
            (0, 0, 'East', 'South'),                   # superior izquierda
            (self.width - 1, 0, 'West', 'South'),      # superior derecha
            (0, self.height - 1, 'East', 'North'),     # inferior izquierda
            (self.width - 1, self.height - 1, 'West', 'North'),
            # inferior derecha
        ]

        # Para cada esquina desempaquetamos su posición y sus paredes internas
        for x, y, dir1, dir2 in corners:
            cell = self.grid[y][x]

            # Si alguna de las dos paredes ya está abierta (False),
            # la esquina ya tiene conexión → pasamos a la siguiente
            if not cell[dir1] or not cell[dir2]:
                continue

            # Si las dos paredes están cerradas (True), la esquina está aislada
            # → calculamos la posición de la celda vecina en dirección dir1
            dx, dy = self.Move[dir1]
            nx, ny = x + dx, y + dy

            # Abrimos la pared dir1 de la esquina
            cell[dir1] = False
            # Abrimos la pared opuesta de la celda vecina (coherencia)
            self.grid[ny][nx][self.opposite_move[dir1]] = False

    def _open_center(self) -> None:
        """Asegura que el centro del laberinto tiene al menos una conexión."""

        cx = self.width // 2
        cy = self.height // 2

        if (cx, cy) in self.pattern_42_cells:
            return

        cell = self.grid[cy][cx]

        # El centro ya tiene una conexión
        if any(not cell[d] for d in self.Move):
            return

        # Buscar una dirección válida que no conecte con el 42
        directions = list(self.Move.items())
        self.rng.shuffle(directions)

        for direction, (dx, dy) in directions:
            nx = cx + dx
            ny = cy + dy

            if not (0 <= nx < self.width and 0 <= ny < self.height):
                continue

            if (nx, ny) in self.pattern_42_cells:
                continue

            opposite = self.opposite_move[direction]

            self.grid[cy][cx][direction] = False
            self.grid[ny][nx][opposite] = False
            return

    def bfs(self) -> List[str]:
        """Encuentra el camino más corto entre entrada y salida usando BFS.

        Devuelve una lista de letras ['N','E','S','W'] que representan
        los movimientos desde la entrada hasta la salida.
        """

        entry = self.entry
        exit_cell = self.exit_cell

        if entry in self.pattern_42_cells:
            raise MazeError("ENTRY cannot be inside the 42 pattern.")

        if exit_cell in self.pattern_42_cells:
            raise MazeError("EXIT cannot be inside the 42 pattern.")

        # Cola BFS: empezamos desde la entrada
        queue = deque([entry])

        # Diccionario que guarda de dónde venimos en cada celda
        # También sirve para saber si ya visitamos
        # una celda (si está como clave)
        came_from: Dict[Tuple[int, int],
                        Optional[Tuple[int, int]]] = {entry: None}

        while queue:
            # Sacamos la celda más antigua de la cola (FIFO)
            current: Optional[Tuple[int, int]] = queue.popleft()

            # Si llegamos a la salida, paramos
            if current == exit_cell:
                break

            # Exploramos los vecinos accesibles (sin pared entre ellos)
            for direction in self.Move:
                dx, dy = self.Move[direction]
                if current is None:
                    break
                cx, cy = current
                nx = cx + dx
                ny = cy + dy

                # Solo añadimos la vecina si: existe, no tiene pared, y
                # no fue visitada
                if (0 <= nx < self.width
                        and 0 <= ny < self.height
                        and self.grid[cy][cx][direction] is False
                        and (nx, ny) not in came_from):
                    came_from[(nx, ny)] = current
                    queue.append((nx, ny))

        # Reconstruimos el camino yendo hacia atrás
        # desde la salida hasta la entrada
        path = []
        while current is not None:
            path.append(current)
            current = came_from[current]

        # Lo damos la vuelta (estaba de salida a entrada,
        # ahora de entrada a salida)
        path.reverse()

        # Traducimos cada par de celdas consecutivas a una letra de dirección
        reverse_move = {v: k for k, v in self.Move.items()}
        result = []
        for i in range(len(path) - 1):
            cx, cy = path[i]
            nx, ny = path[i + 1]
            dx = nx - cx
            dy = ny - cy
            # [0] coge solo la primera letra: 'North'[0] → 'N'
            result.append(reverse_move[(dx, dy)][0])

        return result

    def to_hex(self) -> str:
        """Convierte el grid a formato hexadecimal (una línea por fila).

        Cada celda se convierte a un dígito hex sumando los valores
        de sus paredes cerradas (North=1, East=2, South=4, West=8).
        """

        lines = []

        for row in self.grid:
            line = ''
            for cell in row:
                # Sumamos los valores de las paredes cerradas (True)
                value = 0
                for direction, wall_value in self.walls.items():
                    if cell[direction]:
                        value += wall_value

                # Convertimos el número a hexadecimal en
                #  mayúscula (ej: 13 → 'D')
                line += format(value, 'X')
            lines.append(line)

        # Unimos todas las filas con salto de línea
        return '\n'.join(lines)

    def grid_to_ints(self) -> list[list[int]]:
        """Devuelve grid como enteros (bits) para el display ASCII"""
        int_grid: list[list[int]] = []

        for row in self.grid:
            int_row: list[int] = []
            for cell in row:
                value = 0
                for direction, wall_value in self.walls.items():
                    if cell[direction]:
                        value += wall_value
                int_row.append(value)
            int_grid.append(int_row)

        return int_grid

    def path_to_coords(self, path: list[str]) -> list[tuple[int, int]]:
        """Convierte lista direcciones a cordenadas"""
        x, y = self.entry
        coords: list[tuple[int, int]] = [(x, y)]

        letter_to_move = {
            "N": (0, -1),
            "E": (1, 0),
            "S": (0, 1),
            "W": (-1, 0),
        }

        for step in path:
            try:
                dx, dy = letter_to_move[step]
            except KeyError:
                raise ValueError(
                    f"invalid direction letter {step!r}; expected one of 'N', 'E', 'S', 'W'"
                )
            x += dx
            y += dy
            coords.append((x, y))
        return coords
