"""
Modulo de generacion de laberintos — clase MazeGenerator.
"""
import random
from typing import List, Optional, Tuple, Dict
from collections import deque


class MazeError(Exception):
    """
    Excepcion utilizada para gestionar los errores del objeto maze.
    Args:
        Ninguno.
    Returns:
        Ninguno.
    Raises:
        Ninguna.
    """
    pass


class MazeGenerator:

    walls: Dict[str, int] = {
        'North': 1,
        'East': 2,
        'South': 4,
        'West': 8
    }

    opposite_move: Dict[str, str] = {'North': 'South', 'East': 'West',
                                     'South': 'North', 'West': 'East'}

    Move: Dict[str, Tuple[int, int]] = {
        'North': (0, -1), 'East': (1, 0), 'South': (0, 1), 'West': (-1, 0)
    }

    def __init__(self,
                 width: int,
                 height: int,
                 entry: Tuple[int, int],
                 exit_cell: tuple[int, int],
                 seed: Optional[int] = None) -> None:
        """
        Inicializa el generador con el tamano, la entrada, la salida
        y la semilla.
        Args:
            width: Ancho del laberinto en celdas.
            height: Alto del laberinto en celdas.
            entry: Coordenada de entrada del laberinto.
            exit_cell: Coordenada de salida del laberinto.
            seed: Semilla opcional para la generacion aleatoria.
        Returns:
            Ninguno.
        Raises:
            Ninguna.
        """

        self.pattern_42_cells: List[Tuple[int, int]] = []
        self.width = width
        self.height = height

        self.entry = entry
        self.exit_cell = exit_cell

        if seed is None:
            seed = random.randint(0, 1_000_000)

        self.seed = seed

        self.rng = random.Random(seed)

        self.grid: List[List[dict[str, bool]]] = []

        self.visited: List[List[bool]] = []

    def regenerate(self) -> None:
        """
        Genera una nueva semilla aleatoria y reinicia el generador.
        Args:
            Ninguno.
        Returns:
            Ninguno.
        Raises:
            Ninguna.
        """
        self.seed = random.randint(0, 1_000_000)
        self.rng = random.Random(self.seed)

    def generate(self, perfect: bool = True) -> None:
        """
        Prepara la cuadricula con todas las paredes cerradas y
        lanza el DFS.
        Args:
            perfect: Si es False, el laberinto se convierte en un
                tablero jugable tipo Pac-Man tras el DFS.
        Returns:
            Ninguno.
        Raises:
            Ninguna.
        """

        self.grid = [
            [{"North": True, "East": True, "South": True, "West": True}
                for _ in range(self.width)]
            for _ in range(self.height)
        ]

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
        """
        Genera el laberinto mediante DFS iterativo.
        Args:
            x: Columna de la celda de inicio del DFS.
            y: Fila de la celda de inicio del DFS.
        Returns:
            Ninguno.
        Raises:
            MazeError: Si la celda de inicio esta dentro del patron 42.
        """

        if (x, y) in self.pattern_42_cells:
            raise MazeError("ENTRY cannot be inside the 42 pattern")

        stack = [(x, y)]

        self.visited[y][x] = True

        while stack:
            cx, cy = stack[-1]

            directions = ['North', 'East', 'South', 'West']
            self.rng.shuffle(directions)

            moved = False

            for direction in directions:
                dx, dy = self.Move[direction]
                nx = cx + dx
                ny = cy + dy

                if (0 <= nx < self.width
                        and 0 <= ny < self.height
                        and (nx, ny) not in self.pattern_42_cells
                        and not self.visited[ny][nx]):

                    opposite = self.opposite_move[direction]

                    self.grid[cy][cx][direction] = False
                    self.grid[ny][nx][opposite] = False

                    self.visited[ny][nx] = True

                    stack.append((nx, ny))

                    moved = True
                    break

            if not moved:
                stack.pop()

    def _place_42(self) -> None:
        """
        Dibuja el numero 42 en el centro del laberinto usando celdas
        con todas las paredes cerradas.
        Args:
            Ninguno.
        Returns:
            Ninguno.
        Raises:
            Ninguna.
        """

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

        cells = [
            (x0 + dx, y0 + dy)
            for dx, dy in full_pattern
            if 0 <= x0 + dx < self.width and 0 <= y0 + dy < self.height
        ]

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
        """
        Asegura que el patron 42 queda completamente aislado.
        Args:
            Ninguno.
        Returns:
            Ninguno.
        Raises:
            Ninguna.
        """

        for x, y in self.pattern_42_cells:
            for direction in self.Move:
                self.grid[y][x][direction] = True

            for direction, (dx, dy) in self.Move.items():
                nx = x + dx
                ny = y + dy

                if (0 <= nx < self.width
                        and 0 <= ny < self.height):
                    opposite = self.opposite_move[direction]
                    self.grid[ny][nx][opposite] = True

    def _braid(self, max_dead_ends: int = 2) -> None:
        """
        Elimina callejones sin salida derribando paredes hasta que
        queden como maximo max_dead_ends.
        Args:
            max_dead_ends: Numero maximo de callejones sin salida
                que se toleran al finalizar.
        Returns:
            Ninguno.
        Raises:
            Ninguna.
        """

        def is_dead_end(x: int, y: int) -> bool:
            """
            Comprueba si una celda es un callejon sin salida.
            Args:
                x: Columna de la celda.
                y: Fila de la celda.
            Returns:
                True si la celda tiene una unica pared abierta.
            Raises:
                Ninguna.
            """
            cell = self.grid[y][x]
            open_walls = sum(1 for v in cell.values() if v is False)
            return open_walls == 1

        def get_closed_neighbors(x: int, y: int) -> List[Tuple[str, int, int]]:
            """
            Obtiene los vecinos accesibles con pared cerrada entre ellos.
            Args:
                x: Columna de la celda.
                y: Fila de la celda.
            Returns:
                Lista de tuplas (direccion, columna, fila) de los
                vecinos candidatos.
            Raises:
                Ninguna.
            """
            neighbors = []
            for direction, (dx, dy) in self.Move.items():
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.width
                        and 0 <= ny < self.height
                        and self.grid[y][x][direction] is True
                        and (nx, ny) not in self.pattern_42_cells):
                    neighbors.append((direction, nx, ny))
            return neighbors

        while True:
            dead_ends = [
                (x, y)
                for y in range(self.height)
                for x in range(self.width)
                if (x, y) not in self.pattern_42_cells
                and is_dead_end(x, y)
            ]

            if len(dead_ends) <= max_dead_ends:
                break

            self.rng.shuffle(dead_ends)

            for x, y in dead_ends:
                if not is_dead_end(x, y):
                    continue

                neighbors = get_closed_neighbors(x, y)
                if not neighbors:
                    continue

                direction, nx, ny = self.rng.choice(neighbors)
                opposite = self.opposite_move[direction]
                self.grid[y][x][direction] = False
                self.grid[ny][nx][opposite] = False

    def _make_imperfect(self, probability: float = 0.3) -> None:
        """
        Convierte el laberinto en un tablero tipo Pac-Man.
        Args:
            probability: Parametro reservado para ajustar la
                probabilidad de generar bucles extra.
        Returns:
            Ninguno.
        Raises:
            Ninguna.
        """

        self._braid()

        self._open_corners()

        self._open_center()

    def _open_corners(self) -> None:
        """
        Asegura que las 4 esquinas tienen al menos una conexion
        abierta.
        Args:
            Ninguno.
        Returns:
            Ninguno.
        Raises:
            Ninguna.
        """

        corners = [
            (0, 0, 'East', 'South'),
            (self.width - 1, 0, 'West', 'South'),
            (0, self.height - 1, 'East', 'North'),
            (self.width - 1, self.height - 1, 'West', 'North'),
        ]

        for x, y, dir1, dir2 in corners:
            cell = self.grid[y][x]

            if not cell[dir1] or not cell[dir2]:
                continue

            dx, dy = self.Move[dir1]
            nx, ny = x + dx, y + dy

            cell[dir1] = False
            self.grid[ny][nx][self.opposite_move[dir1]] = False

    def _open_center(self) -> None:
        """
        Asegura que el centro del laberinto tiene al menos una
        conexion.
        Args:
            Ninguno.
        Returns:
            Ninguno.
        Raises:
            Ninguna.
        """

        cx = self.width // 2
        cy = self.height // 2

        if (cx, cy) in self.pattern_42_cells:
            return

        cell = self.grid[cy][cx]

        if any(not cell[d] for d in self.Move):
            return

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
        """
        Encuentra el camino mas corto entre la entrada y la salida
        mediante BFS.
        Args:
            Ninguno.
        Returns:
            Lista de letras ('N', 'E', 'S', 'W') con los movimientos
            desde la entrada hasta la salida.
        Raises:
            MazeError: Si la entrada o la salida estan dentro del
                patron 42.
        """

        entry = self.entry
        exit_cell = self.exit_cell

        if entry in self.pattern_42_cells:
            raise MazeError("ENTRY cannot be inside the 42 pattern.")

        if exit_cell in self.pattern_42_cells:
            raise MazeError("EXIT cannot be inside the 42 pattern.")

        queue = deque([entry])

        came_from: Dict[Tuple[int, int],
                        Optional[Tuple[int, int]]] = {entry: None}

        while queue:
            current: Optional[Tuple[int, int]] = queue.popleft()

            if current == exit_cell:
                break

            for direction in self.Move:
                dx, dy = self.Move[direction]
                if current is None:
                    break
                cx, cy = current
                nx = cx + dx
                ny = cy + dy

                if (0 <= nx < self.width
                        and 0 <= ny < self.height
                        and self.grid[cy][cx][direction] is False
                        and (nx, ny) not in came_from):
                    came_from[(nx, ny)] = current
                    queue.append((nx, ny))

        path = []
        while current is not None:
            path.append(current)
            current = came_from[current]

        path.reverse()

        reverse_move = {v: k for k, v in self.Move.items()}
        result = []
        for i in range(len(path) - 1):
            cx, cy = path[i]
            nx, ny = path[i + 1]
            dx = nx - cx
            dy = ny - cy
            result.append(reverse_move[(dx, dy)][0])

        return result

    def to_hex(self) -> str:
        """
        Convierte la cuadricula a formato hexadecimal, una linea
        por fila.
        Args:
            Ninguno.
        Returns:
            Cadena con el laberinto codificado en hexadecimal,
            sumando los valores de las paredes cerradas de cada
            celda (North=1, East=2, South=4, West=8).
        Raises:
            Ninguna.
        """

        lines = []

        for row in self.grid:
            line = ''
            for cell in row:
                value = 0
                for direction, wall_value in self.walls.items():
                    if cell[direction]:
                        value += wall_value

                line += format(value, 'X')
            lines.append(line)

        return '\n'.join(lines)

    def grid_to_ints(self) -> list[list[int]]:
        """
        Convierte la cuadricula a enteros para el display ASCII.
        Args:
            Ninguno.
        Returns:
            Cuadricula donde cada celda es un entero (bits) que
            representa sus paredes cerradas.
        Raises:
            Ninguna.
        """
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
        """
        Convierte una lista de direcciones en coordenadas.
        Args:
            path: Lista de letras de direccion ('N', 'E', 'S', 'W').
        Returns:
            Lista de coordenadas (x, y) desde la entrada hasta el
            final del camino.
        Raises:
            ValueError: Si alguna letra de direccion no es valida.
        """
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
                    f"invalid direction letter {step!r};"
                    "expected one of 'N', 'E', 'S', 'W'"
                )
            x += dx
            y += dy
            coords.append((x, y))
        return coords
