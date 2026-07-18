"""Maze generation module — MazeGenerator class."""
import random
from typing import List, Optional, Tuple, Dict
from collections import deque


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

    def generate(self) -> None:
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

        # Lanzamos el DFS desde la celda de entrada
        entry_x, entry_y = self.entry
        self._carve(entry_x, entry_y)

    def _carve(self, x: int, y: int) -> None:
        """Algoritmo DFS recursivo que genera el laberinto derribando paredes.

        Marca la celda actual como visitada, baraja las direcciones
        aleatoriamente y excava hacia las celdas vecinas no visitadas.
        El backtracking ocurre automáticamente al
        terminar cada llamada recursiva.
        """

        # Marcamos la celda actual como visitada
        self.visited[y][x] = True

        # Barajamos las direcciones para generar un laberinto aleatorio
        directions = ['North', 'East', 'South', 'West']
        self.rng.shuffle(directions)

        for direction in directions:
            # Calculamos el desplazamiento y la posición de la celda vecina
            dx, dy = self.Move[direction]
            nx = x + dx
            ny = y + dy

            # Solo avanzamos si la vecina existe y no fue visitada
            if (0 <= nx < self.width
                    and 0 <= ny < self.height
                    and not self.visited[ny][nx]):

                # Derribamos la pared entre la celda actual y la vecina
                # (hay que actualizar las DOS celdas para mantener coherencia)
                opposite = self.opposite_move[direction]
                self.grid[y][x][direction] = False
                self.grid[ny][nx][opposite] = False

                # Llamada recursiva: nos movemos a la celda vecina
                self._carve(nx, ny)

    def _place_42(self) -> None:
        """Dibuja el número 42 en el centro del laberinto
        usando celdas con todas las paredes cerradas."""

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

        for dx, dy in full_pattern:
            x_real = x0 + dx
            y_real = y0 + dy
            if (0 <= x_real < self.width
                    and 0 <= y_real < self.height):
                self.grid[y_real][x_real] = {
                    "North": True,
                    "East": True,
                    "South": True,
                    "West": True
                }

    def _add_loops(self, probability: float = 0.3) -> None:
        """Derriba paredes extra aleatoriamente para crear
        múltiples caminos."""

        # Recorremos cada fila del laberinto
        for y in range(self.height):
            # Recorremos cada columna de esa fila
            for x in range(self.width):

                # Intentamos derribar la pared Este:
                # - que exista celda vecina al Este (no es borde derecho)
                # - que la pared Este esté cerrada (True)
                # - que el número aleatorio sea menor que probability
                # (30% de veces)
                if (x + 1 < self.width
                        and self.grid[y][x]['East'] is True
                        and self.rng.random() < probability):
                    # Abrimos la pared Este de la celda actual
                    self.grid[y][x]['East'] = False
                    # Abrimos la pared Oeste de la celda vecina (coherencia)
                    self.grid[y][x + 1]['West'] = False

                # Mismo proceso pero para la pared Sur
                if (y + 1 < self.height
                        and self.grid[y][x]['South'] is True
                        and self.rng.random() < probability):
                    # Abrimos la pared Sur de la celda actual
                    self.grid[y][x]['South'] = False
                    # Abrimos la pared Norte de la celda de abajo (coherencia)
                    self.grid[y + 1][x]['North'] = False

    def _make_imperfect(self, probability: float = 0.3) -> None:
        """Convierte el laberinto en un tablero tipo Pac-Man."""

        # Paso 1: crear bucles derribando paredes extra aleatoriamente
        self._add_loops(probability)

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
        """Asegura que el centro del laberinto tiene al
        menos una conexión abierta."""

        # Calculamos las coordenadas del centro del laberinto
        cx = self.width // 2
        cy = self.height // 2

        # Accedemos a la celda central (recuerda: [fila][columna] = [y][x])
        cell = self.grid[cy][cx]

        # Si ya tiene alguna pared abierta (False), no hacemos nada
        # any() devuelve True si al menos UNA condición es True
        if any(not cell[d] for d in ['North', 'East', 'South', 'West']):
            return

        # Si está completamente cerrada (puede pasar si cae
        # dentro del patrón 42)
        # abrimos la pared Este y la pared Oeste de su vecina (coherencia)
        self.grid[cy][cx]['East'] = False
        self.grid[cy][cx + 1]['West'] = False

    def bfs(self) -> List[str]:
        """Encuentra el camino más corto entre entrada y salida usando BFS.

        Devuelve una lista de letras ['N','E','S','W'] que representan
        los movimientos desde la entrada hasta la salida.
        """

        entry = self.entry
        exit_cell = self.exit_cell

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
