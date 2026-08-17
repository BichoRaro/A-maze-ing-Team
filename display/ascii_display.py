"""
Modulo de visualizacion ASCII del proyecto A-Maze-ing.
"""
from typing import List, Tuple

Coord = Tuple[int, int]

COLORS = [
    "\033[37m",
    "\033[31m",
    "\033[32m",
    "\033[33m",
    "\033[34m",
    "\033[35m",
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

        self.wall_color = "\033[37m"
        self.reset_color = "\033[0m"

        self.bg_open = "\033[40m"

        self.bg_42 = "\033[100m"

    def render(self) -> None:
        """
        Renderiza el laberinto completo en la terminal.
        Args:
            Ninguno.
        Returns:
            Ninguno.
        Raises:
            Ninguna.
        """

        height = len(self.grid)

        for y in range(height):
            top_line = self._render_top_line(y)
            mid_line = self._render_mid_line(y)

            print(top_line)
            print(mid_line)

        bottom_line = self._render_bottom_line()
        print(bottom_line)

    def toggle_path(self) -> None:
        """
        Muestra u oculta el camino mas corto.
        Args:
            Ninguno.
        Returns:
            Ninguno.
        Raises:
            Ninguna.
        """
        self.show_path = not self.show_path

    def set_wall_color(self, color_code: str) -> None:
        """
        Cambia el color de las paredes.
        Args:
            color_code: Codigo ANSI del color a aplicar.
        Returns:
            Ninguno.
        Raises:
            Ninguna.
        """
        self.wall_color = color_code

    def rotate_color(self) -> None:
        """
        Rota al siguiente color disponible de la lista.
        Args:
            Ninguno.
        Returns:
            Ninguno.
        Raises:
            Ninguna.
        """
        self.color_index = (self.color_index + 1) % len(COLORS)
        self.wall_color = COLORS[self.color_index]

    def _cell_has_wall_north(self, value: int) -> bool:
        """
        Comprueba si la celda tiene pared en el lado Norte.
        Args:
            value: Valor entero de la celda.
        Returns:
            True si la pared Norte esta cerrada.
        Raises:
            Ninguna.
        """
        return bool(value & 1)

    def _cell_has_wall_east(self, value: int) -> bool:
        """
        Comprueba si la celda tiene pared en el lado Este.
        Args:
            value: Valor entero de la celda.
        Returns:
            True si la pared Este esta cerrada.
        Raises:
            Ninguna.
        """
        return bool(value & 2)

    def _cell_has_wall_south(self, value: int) -> bool:
        """
        Comprueba si la celda tiene pared en el lado Sur.
        Args:
            value: Valor entero de la celda.
        Returns:
            True si la pared Sur esta cerrada.
        Raises:
            Ninguna.
        """
        return bool(value & 4)

    def _cell_has_wall_west(self, value: int) -> bool:
        """
        Comprueba si la celda tiene pared en el lado Oeste.
        Args:
            value: Valor entero de la celda.
        Returns:
            True si la pared Oeste esta cerrada.
        Raises:
            Ninguna.
        """
        return bool(value & 8)

    def _vertical_wall(self, y: int, x: int) -> bool:
        """
        Comprueba si existe una pared vertical en una posicion dada.
        Args:
            y: Fila de la celda.
            x: Columna que actua como frontera entre celdas.
        Returns:
            True si hay una pared vertical en esa frontera.
        Raises:
            Ninguna.
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
        Devuelve el caracter correcto para una interseccion.
        Args:
            left: True si hay conexion hacia la izquierda.
            right: True si hay conexion hacia la derecha.
            up: True si hay conexion hacia arriba.
            down: True si hay conexion hacia abajo.
        Returns:
            Caracter que representa la interseccion resultante.
        Raises:
            Ninguna.
        """

        connections = (left, right, up, down)

        chars = {
            (False, False, False, False): " ",

            (True, False, False, False): "─",
            (False, True, False, False): "─",
            (False, False, True, False): "│",
            (False, False, False, True): "│",

            (True, True, False, False): "─",
            (False, False, True, True): "│",

            (False, True, False, True): "┌",
            (True, False, False, True): "┐",
            (False, True, True, False): "└",
            (True, False, True, False): "┘",

            (True, True, False, True): "┬",
            (True, True, True, False): "┴",
            (True, False, True, True): "┤",
            (False, True, True, True): "├",

            (True, True, True, True): "┼",
        }

        return chars[connections]

    def _render_top_line(self, y: int) -> str:
        """
        Dibuja la linea superior de una fila del laberinto.
        Args:
            y: Fila que se va a dibujar.
        Returns:
            Cadena con las paredes horizontales y las intersecciones.
        Raises:
            Ninguna.
        """

        width = len(self.grid[0])
        line = ""

        for x in range(width + 1):

            left = (
                x > 0
                and self._cell_has_wall_north(self.grid[y][x - 1])
            )

            right = (
                x < width
                and self._cell_has_wall_north(self.grid[y][x])
            )

            up = (
                y > 0
                and self._vertical_wall(y - 1, x)
            )

            down = self._vertical_wall(y, x)

            line += self.wall_color
            line += self._junction(left, right, up, down)
            line += self.reset_color

            if x < width:
                if self._cell_has_wall_north(self.grid[y][x]):
                    line += self.wall_color + "───" + self.reset_color
                else:
                    line += "   "

        return line

    def _render_mid_line(self, y: int) -> str:
        """
        Dibuja el contenido de las celdas de una fila.
        Args:
            y: Fila que se va a dibujar.
        Returns:
            Cadena con el contenido y las paredes verticales de la fila.
        Raises:
            Ninguna.
        """

        width = len(self.grid[0])
        line = ""

        for x in range(width):

            if self._vertical_wall(y, x):
                line += self.wall_color + "│" + self.reset_color
            else:
                line += " "

            coord = (x, y)

            if coord in self.pattern_42:
                line += self.bg_42 + "   " + self.reset_color

            elif coord == self.entry:
                line += "\033[45m S \033[0m"

            elif coord == self.exit:
                line += "\033[41m E \033[0m"

            elif self.show_path and coord in self.shortest_path:
                line += "\033[46m   \033[0m"

            else:
                line += self.bg_open + "   " + self.reset_color

        if self._vertical_wall(y, width):
            line += self.wall_color + "│" + self.reset_color
        else:
            line += " "

        return line

    def _render_bottom_line(self) -> str:
        """
        Dibuja la ultima linea horizontal del laberinto.
        Args:
            Ninguno.
        Returns:
            Cadena con la linea inferior del laberinto.
        Raises:
            Ninguna.
        """

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
