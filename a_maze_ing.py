from display.ascii_display import AsciiDisplay

def main() -> None:
    grid = generator.grid
    entry = generator.entry
    exit = generator.exit
    path = generator.shortest_path

    display = AsciiDisplay(grid, entry, exit, path)
    display.render()
