from typing import List, Tuple

Coord = Tuple[int, int]


class AsciiDisplay:
    def __init__(
            self,
            grid: List[List[int]],
            entry: Coord,
            exit: Coord,
            shortest_path: List[Coord],
        ) -> None:
            self.grid = grid    # matriz de celdas, cada int = bits de paredes
            self.entry = entry
            self.exit = exit
            self.shortest_path = shortest_path
            self.show_path = False  # toggle para mostrar/ocultar camino
            self.wall_color = ""    # "\033[37m"    # blanco
            self.reset_color = ""   # "\033[0m"
    
    def render(self) -> None:
        """Render the entire maze tot he terminal as ASCII"""
        height = len(self.grid)

        # Emepzams con una linea superior completa (N de a primera fila)
        for y in range(height):
            top_line, mid_line = self._render_row(y)
            print(top_line)
            print(mid_line)

        # Dibujar la linea inferior usanod las paredes S de la ultima fila
        bottom_line = ""
        width = len(self.grid[0])
        last_row_index = height - 1
        
        for x in range(width):
            cell_value = self.grid[last_row_index][x]
            bottom_line += self.wall_color + "+" + self.reset_color
            if self._cell_has_wall_south(cell_value):
                bottom_line += self.wall_color + "---" + self.reset_color
            else:
                bottom_line += "   "
        bottom_line += self.wall_color + "+" + self.reset_color
        print(bottom_line)

    def toggle_path(self) -> None:
        self.show_path = not self.show_path

    def set_wall_color(self, color_code: str) -> None:
        self.wall_color = color_code

    def run_menu(self) -> None:
        """Bucle interactivo con opciones 1-4"""
    
    def _cell_has_wall_north(self, value: int) -> bool:
        """Return True if the cell has a Norht wall ( bit 0 == 1)."""
        return bool(value & 1)

    def _cell_has_wall_east(self, value: int) -> bool:
        """Return True if the cell has a East wall ( bit 1 == 1)."""
        return bool(value & 2)

    def _cell_has_wall_south(self, value: int) -> bool:
        """Return True if the cell has a South wall ( bit 2 == 1)."""
        return bool(value & 4)

    def _cell_has_wall_west(self, value: int) -> bool:
        """Return True if the cell has a West wall ( bit 3 == 1)."""
        return bool(value & 8)

    def _render_row(self, y: int) -> tuple[str, str]:
        """Render one maze row (top walls and middle content) for row y."""
        top_line = ""
        mid_line = ""

        width = len(self.grid[0])

        for x in range(width):
            cell_value = self.grid[y][x]
            # Top walls North
            # siempre dibujamos un '+', y luego '---' si hay pared N, o '   '
            # si esta abierto.
            top_line += self.wall_color + "+" + self.reset_color
            if self._cell_has_wall_north(cell_value):
                top_line += self.wall_color + "---" + self.reset_color
            else:
                top_line += "   "
            
            # Middle line (west wall + cell content + East wall)
            # West wall
            if self._cell_has_wall_west(cell_value):
                mid_line += self.wall_color + "|" + self.reset_color
            else:
                mid_line += " "

            coord = (x, y)
            if coord == self.entry:
                char = "E" # entrada
            elif coord == self.exit:
                char = "X" # salida
            elif self.show_path and coord in self.shortest_path:
                char = "." # parte del camino
            else:
                char = " " # celda normal

            mid_line += f" {char} "

            # East wall
            if self._cell_has_wall_east(cell_value):
                mid_line += self.wall_color + "|" + self.reset_color
            else:
                mid_line += " "

        # Cerrara la fila con un '+' al final de la linea superior
        top_line += self.wall_color + "+" + self.reset_color

        return top_line, mid_line
