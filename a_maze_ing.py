import sys

from display.ascii_display import AsciiDisplay
from mazegen.generator import MazeGenerator
from parse_config import parse_config, ConfigError


def main() -> None:
    # Comprovamos que tengamos un archivo para leer
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        return

    config_path = sys.argv[1]

    # Pasamos el parseo
    try:
        config = parse_config(config_path)
    except ConfigError as exc:
        print(f"Configuration error: {exc}")
        return
    
    width = config["width"]
    height = config["height"]
    entry = config["entry"]     # (x, y)
    exit_cell = config["exit"]   # (x, y)
    perfect = config["perfect"]
    output_file = config["output_file"]
    seed = config["seed"]


    maze = MazeGenerator(
        width=width,
        height=height,
        entry=entry,
        exit_cell=exit_cell,
        seed=seed,
    )

    maze.generate(perfect=perfect)
    
    # Mapa en fomrato hex + camino en letras
    hex_map = maze.to_hex()
    path_letters = maze.bfs()
    
    int_grid = maze.grid_to_ints()
    path_coords = maze.path_to_coords(path_letters)


    grid = [
        [9,  3],
        [8,  2],
        [8,  2],
        [12, 6],
    ]

    entry = (0, 0)
    exit = (1, 3)
    shortest_path = [(0, 0), (1, 0), (1, 1), (1, 2), (2, 2), (3, 2), (3, 3)]

    display = AsciiDisplay(
        grid=int_grid, 
        entry=entry, 
        exit=exit_cell, 
        shortest_path= path_coords
    )

    # Primero sin mostrar el camino
    display.show_path = False
    print("Maze without path:")
    display.render()

    # Luego activando el camino
    display.show_path = True
    print("\nMaze with path:")
    display.render()


if __name__ == "__main__":
    main()
