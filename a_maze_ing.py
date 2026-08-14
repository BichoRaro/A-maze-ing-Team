import sys
from display.ascii_display import AsciiDisplay
from mazegen.generator import MazeGenerator
from parse_config import parse_config, ConfigError
from output_writer import write_output
from typing import Any, Dict, Tuple


def run_menu(config: Dict[str, Any], maze: MazeGenerator, display: AsciiDisplay) -> None:
    """Bucle interactivo con el usuario."""
    while True:
        print("\n=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show / Hide the shortest path")
        print("3. Rotate the wall colours")
        print("4. Quit")
        choice = input("Choice? (1-4): ").strip()

        if choice == "1":
            # Re-generar: usar el MISMO maze y MISMO display
            width = config["width"]
            height = config["height"]
            entry = config["entry"]
            exit_cell = config["exit"]
            perfect = config["perfect"]
            output_file = config["output_file"]

            maze.generate(perfect=perfect)
            hex_map = maze.to_hex()
            path_letters = maze.bfs()
            int_grid = maze.grid_to_ints()
            path_coords = maze.path_to_coords(path_letters)

            write_output(output_file, hex_map, entry, exit_cell, path_letters)

            display.grid = int_grid
            display.shortest_path = path_coords
            display.show_path = False
            display.render()

        elif choice == "2":
            display.toggle_path()
            display.render()

        elif choice == "3":
            display.rotate_color()
            display.render()

        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-4.")


def build_maze(config: Dict[str, Any]) -> Tuple [MazeGenerator, AsciiDisplay,
                                                             list[str]]:
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
        shortest_path=path_coords,
        pattern_42=maze.pattern_42_cells
    )
    display.show_path = False
    display.render()

    return maze, display, path_letters


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

    maze, display, _ = build_maze(config)

    run_menu(config, maze, display)


if __name__ == "__main__":
    main()
