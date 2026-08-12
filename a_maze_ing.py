import sys
from display.ascii_display import AsciiDisplay
from mazegen.generator import MazeGenerator
from parse_config import parse_config, ConfigError
from output_writer import write_output


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        return

    config_path = sys.argv[1]

    try:
        config = parse_config(config_path)
    except ConfigError as exc:
        print(f"Configuration error: {exc}")
        return

    width = config["width"]
    height = config["height"]
    entry = config["entry"]
    exit_cell = config["exit"]
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

    hex_map = maze.to_hex()
    path_letters = maze.bfs()
    int_grid = maze.grid_to_ints()
    path_coords = maze.path_to_coords(path_letters)

    # Escribir fichero de salida
    write_output(output_file, hex_map, entry, exit_cell, path_letters)

    # Mostrar laberinto y menú interactivo
    display = AsciiDisplay(
        grid=int_grid,
        entry=entry,
        exit=exit_cell,
        shortest_path=path_coords
    )
    display.show_path = False
    display.render()


if __name__ == "__main__":
    main()
