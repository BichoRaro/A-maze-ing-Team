"""ASCII display module for the A-Maze-ing project."""
from typing import List, Tuple

Coord = Tuple[int, int]

COLORS = [
    "\033[37m",   # blanco
    "\033[31m",   # rojo
    "\033[32m",   # verde
    "\033[33m",   # amarillo
    "\033[34m",   # azul
    "\033[35m",   # magenta
]


class AsciiDisplay:
    def __init__(
            self,
            grid: List[List[int]],
            entry: Coord,
            exit: Coord,
            shortest_path: List[Coord],
            pattern_42: List[Coord],
    ) -> None:
        self.grid = grid
        self.entry = entry
        self.exit = exit
        self.shortest_path = shortest_path
        self.pattern_42 = pattern_42
        self.show_path = False
        self.color_index = 0

        # Color de las paredes
        self.wall_color = "\033[37m"
        self.reset_color = "\033[0m"

        # Fondo de las celdas
        self.bg_open = "\033[40m"

        # Color del 42
        self.bg_42 = "\033[100m"

    def render(self) -> None:
        """Renderiza el laberinto completo en la terminal."""

        height = len(self.grid)

        for y in range(height):
            top_line = self._render_top_line(y)
            mid_line = self._render_mid_line(y)

            print(top_line)
            print(mid_line)

        # Última línea horizontal
        bottom_line = self._render_bottom_line()
        print(bottom_line)

    def toggle_path(self) -> None:
        """Muestra u oculta el camino más corto."""
        self.show_path = not self.show_path

    def set_wall_color(self, color_code: str) -> None:
        """Cambia el color de las paredes."""
        self.wall_color = color_code

    def rotate_color(self) -> None:
        """Rota al siguiente color de la lista."""
        self.color_index = (self.color_index + 1) % len(COLORS)
        self.wall_color = COLORS[self.color_index]

    # ---------------------------------------------------------
    # PAREDES
    # ---------------------------------------------------------

    def _cell_has_wall_north(self, value: int) -> bool:
        """True si la celda tiene pared Norte."""
        return bool(value & 1)

    def _cell_has_wall_east(self, value: int) -> bool:
        """True si la celda tiene pared Este."""
        return bool(value & 2)

    def _cell_has_wall_south(self, value: int) -> bool:
        """True si la celda tiene pared Sur."""
        return bool(value & 4)

    def _cell_has_wall_west(self, value: int) -> bool:
        """True si la celda tiene pared Oeste."""
        return bool(value & 8)

    def _vertical_wall(self, y: int, x: int) -> bool:
        """
        Comprueba si existe una pared vertical en una posición.

        x representa la frontera entre columnas.
        """

        width = len(self.grid[0])

        if x == 0:
            return self._cell_has_wall_west(self.grid[y][0])

        if x == width:
            return self._cell_has_wall_east(
                self.grid[y][width - 1]
            )

        return (
            self._cell_has_wall_east(self.grid[y][x - 1])
            or self._cell_has_wall_west(self.grid[y][x])
        )

    def _junction(
            self,
            left: bool,
            right: bool,
            up: bool,
            down: bool,
    ) -> str:
        """
        Devuelve el carácter correcto para una intersección.

        Orden:
            left, right, up, down
        """

        connections = (left, right, up, down)

        chars = {
            (False, False, False, False): " ",

            # Una sola dirección
            (True, False, False, False): "─",
            (False, True, False, False): "─",
            (False, False, True, False): "│",
            (False, False, False, True): "│",

            # Dos direcciones
            (True, True, False, False): "─",
            (False, False, True, True): "│",

            (False, True, False, True): "┌",
            (True, False, False, True): "┐",
            (False, True, True, False): "└",
            (True, False, True, False): "┘",

            # Tres direcciones
            (True, True, False, True): "┬",
            (True, True, True, False): "┴",
            (True, False, True, True): "┤",
            (False, True, True, True): "├",

            # Cuatro direcciones
            (True, True, True, True): "┼",
        }

        return chars[connections]

    def _render_top_line(self, y: int) -> str:
        """
        Dibuja la línea superior de una fila.

        Aquí aparecen las paredes horizontales y
        las intersecciones.
        """

        width = len(self.grid[0])
        line = ""

        for x in range(width + 1):

            # ¿Hay pared hacia la izquierda?
            left = (
                x > 0
                and self._cell_has_wall_north(self.grid[y][x - 1])
            )

            # ¿Hay pared hacia la derecha?
            right = (
                x < width
                and self._cell_has_wall_north(self.grid[y][x])
            )

            # ¿Hay pared vertical arriba?
            up = (
                y > 0
                and self._vertical_wall(y - 1, x)
            )

            # ¿Hay pared vertical abajo?
            down = self._vertical_wall(y, x)

            line += self.wall_color
            line += self._junction(left, right, up, down)
            line += self.reset_color

            # Segmento horizontal
            if x < width:
                if self._cell_has_wall_north(self.grid[y][x]):
                    line += self.wall_color + "───" + self.reset_color
                else:
                    line += "   "

        return line

    def _render_mid_line(self, y: int) -> str:
        """Dibuja el contenido de las celdas."""

        width = len(self.grid[0])
        line = ""

        for x in range(width):

            # Pared izquierda
            if self._vertical_wall(y, x):
                line += self.wall_color + "│" + self.reset_color
            else:
                line += " "

            coord = (x, y)

            # -------------------------------------------------
            # 42
            # -------------------------------------------------

            if coord in self.pattern_42:
                line += self.bg_42 + "   " + self.reset_color

            # -------------------------------------------------
            # ENTRADA
            # -------------------------------------------------

            elif coord == self.entry:
                line += "\033[45m S \033[0m"

            # -------------------------------------------------
            # SALIDA
            # -------------------------------------------------

            elif coord == self.exit:
                line += "\033[41m E \033[0m"

            # -------------------------------------------------
            # CAMINO
            # -------------------------------------------------

            elif self.show_path and coord in self.shortest_path:
                line += "\033[46m   \033[0m"

            # -------------------------------------------------
            # CELDA VACÍA
            # -------------------------------------------------

            else:
                line += self.bg_open + "   " + self.reset_color

        # Última pared vertical
        if self._vertical_wall(y, width):
            line += self.wall_color + "│" + self.reset_color
        else:
            line += " "

        return line

    def _render_bottom_line(self) -> str:
        """Dibuja la última línea del laberinto."""

        width = len(self.grid[0])
        y = len(self.grid) - 1

        line = ""

        for x in range(width + 1):

            left = (
                x > 0
                and self._cell_has_wall_south(self.grid[y][x - 1])
            )

            right = (
                x < width
                and self._cell_has_wall_south(self.grid[y][x])
            )

            up = self._vertical_wall(y, x)
            down = False

            line += self.wall_color
            line += self._junction(left, right, up, down)
            line += self.reset_color

            if x < width:
                if self._cell_has_wall_south(self.grid[y][x]):
                    line += self.wall_color + "───" + self.reset_color
                else:
                    line += "   "

        return line
