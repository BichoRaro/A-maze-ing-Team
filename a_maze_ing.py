import os
import sys

from typing import Any, Dict, List, Tuple

from display.ascii_display import AsciiDisplay
from mazegen.generator import MazeGenerator, MazeError
from output_writer import write_output
from parse_config import parse_config, ConfigError


def run_menu(config: Dict[str, Any], maze: MazeGenerator,
             display: AsciiDisplay) -> None:
    """
    Ejecuta el bucle interactivo del menu principal.
    Args:
        config: Diccionario con la configuracion del laberinto.
        maze: Instancia del generador de laberintos en uso.
        display: Instancia encargada de renderizar el laberinto.
    Returns:
        Ninguno.
    Raises:
        Ninguna.
    """
    while True:
        os.system('clear')
        display.render()
        print("\n=== A-Maze-ing ===")
        print(f"Your seed: {maze.seed}")
        print("1. Re-generate a new maze")
        print("2. Show / Hide the shortest path")
        print("3. Rotate the wall colours")
        print("4. Quit")
        try:
            choice = input("Choice? (1-4): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if choice == "1":
            maze.regenerate()
            entry = config["entry"]
            exit_cell = config["exit"]
            perfect = config["perfect"]
            output_file = config["output_file"]

            try:
                maze.generate(perfect=perfect)
                hex_map = maze.to_hex()
                path_letters = maze.bfs()
                int_grid = maze.grid_to_ints()
                path_coords = maze.path_to_coords(path_letters)

                write_output(output_file, hex_map, entry,
                             exit_cell, path_letters)
            except MazeError as e:
                print(f"Error regenerating maze: {e}")
                continue
            except OSError as e:
                print(f"Failed writing output file '{output_file}': {e}")
                continue

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


def build_maze(config: Dict[str, Any]) -> Tuple[
    MazeGenerator, AsciiDisplay, List[str]
]:
    try:
        width = config["width"]
        height = config["height"]
        entry = config["entry"]
        exit_cell = config["exit"]
        perfect = config["perfect"]
        output_file = config["output_file"]
        seed = config["seed"]
    except KeyError as e:
        raise MazeError(f"Missing config key: {e}") from e

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

    try:
        write_output(output_file, hex_map, entry, exit_cell, path_letters)
    except OSError as e:
        raise MazeError(
            f"Failed writing output file '{output_file}': {e}"
        ) from e

    display = AsciiDisplay(
        grid=int_grid,
        entry=entry,
        exit=exit_cell,
        shortest_path=path_coords,
        pattern_42=maze.pattern_42_cells,
    )
    display.show_path = False

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
    except (OSError, UnicodeDecodeError) as exc:
        print(f"Could not read config file '{config_path}': {exc}")
        return

    try:
        maze, display, _ = build_maze(config)
        run_menu(config, maze, display)
    except KeyboardInterrupt:
        print("\nProceso interrumpido por el usuario.")
        return
    except MazeError as e:
        print(f"Error: {e}")
        return


if __name__ == "__main__":
    main()
