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
        self.wall_color = "\033[37m"
        self.reset_color = "\033[0m"
        self.bg_open = "\033[40m"
        self.bg_42 = "\033[100m"

    def render(self) -> None:
        """Renderiza el laberinto completo en la terminal."""
        height = len(self.grid)

        for y in range(height):
            top_line, mid_line = self._render_row(y)
            print(top_line)
            print(mid_line)

        bottom_line = ""
        width = len(self.grid[0])
        last_row = height - 1

        for x in range(width):
            cell_value = self.grid[last_row][x]
            bottom_line += self.wall_color + "█" + self.reset_color
            if self._cell_has_wall_south(cell_value):
                bottom_line += self.wall_color + "███" + self.reset_color
            else:
                bottom_line += self.bg_open + "   " + self.reset_color
        bottom_line += self.wall_color + "█" + self.reset_color
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

    def _cell_has_wall_north(self, value: int) -> bool:
        """True si la celda tiene pared Norte (bit 0)."""
        return bool(value & 1)

    def _cell_has_wall_east(self, value: int) -> bool:
        """True si la celda tiene pared Este (bit 1)."""
        return bool(value & 2)

    def _cell_has_wall_south(self, value: int) -> bool:
        """True si la celda tiene pared Sur (bit 2)."""
        return bool(value & 4)

    def _cell_has_wall_west(self, value: int) -> bool:
        """True si la celda tiene pared Oeste (bit 3)."""
        return bool(value & 8)

    def _render_row(self, y: int) -> Tuple[str, str]:
        """Renderiza una fila del laberinto (paredes Norte y contenido)."""
        top_line = ""
        mid_line = ""
        width = len(self.grid[0])

        for x in range(width):
            cell_value = self.grid[y][x]
            coord = (x, y)

            # Pared Norte
            top_line += self.wall_color + "█" + self.reset_color
            if self._cell_has_wall_north(cell_value):
                top_line += self.wall_color + "███" + self.reset_color
            else:
                top_line += self.bg_open + "   " + self.reset_color

            # Pared Oeste
            if self._cell_has_wall_west(cell_value):
                mid_line += self.wall_color + "█" + self.reset_color
            else:
                mid_line += self.bg_open + " " + self.reset_color

            # Contenido de la celda
            if coord in self.pattern_42:
                mid_line += "\033[100m   \033[0m"   # gris oscuro brillante
            elif coord == self.entry:
                mid_line += "\033[45m   \033[0m"    # bloque magenta/rosa
            elif coord == self.exit:
                mid_line += "\033[41m   \033[0m"    # bloque rojo
            elif self.show_path and coord in self.shortest_path:
                mid_line += "\033[46m   \033[0m"    # bloque cian
            else:
                mid_line += self.bg_open + "   " + self.reset_color

        # Cerrar la fila con el borde derecho
        top_line += self.wall_color + "█" + self.reset_color
        mid_line += self.wall_color + "█" + self.reset_color

        return top_line, mid_line
