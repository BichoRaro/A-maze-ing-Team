from typing import import List, Tuple


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
            self.wall_color = "\033[37m"    # blanco
            self.reset_color = "\033[0m"
    
    def render(self) -> None:
        """Dibujar laberinto"""
        print("ASCII maze rendering not implemented yet.")

    def toggle_path(self) -> None:
        self.show_path = not self.show_path

    def set_wall_color(self, color_code: str) -> None:
        self.wall_color = color_code

    def run_menu(self) -> None:
        """Bucle interactivo con opciones 1-4"""
