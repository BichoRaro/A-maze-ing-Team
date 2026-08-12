from typing import List, Tuple


def write_output(
    filename: str,
    hex_maze: str,
    entry: Tuple[int, int],
    exit_cell: Tuple[int, int],
    path: List[str]
) -> None:

    with open(filename, 'w') as f:
        f.write(hex_maze + '\n')
        f.write('\n')
        f.write(f"{entry[0]},{entry[1]}\n")
        f.write(f"{exit_cell[0]},{exit_cell[1]}\n")
        f.write(''.join(path) + '\n')
