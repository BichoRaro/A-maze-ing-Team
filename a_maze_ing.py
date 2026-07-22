from display.ascii_display import AsciiDisplay


def main() -> None:
    # En vez de leer config o usar el generador, hacemos una prueba manual:

    grid = [
        [9,  3],
        [8,  2],
        [8,  2], 
        [12, 6],
    ]

    entry = (0, 0)
    exit = (1, 3)
    shortest_path = [(0, 0), (1, 0), (1, 1), (1, 2), (2, 2), (3, 2), (3, 3)]

    display = AsciiDisplay(grid, entry, exit, shortest_path)

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
