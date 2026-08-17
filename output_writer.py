from typing import List, Tuple


def write_output(
    filename: str,
    hex_maze: str,
    entry: Tuple[int, int],
    exit_cell: Tuple[int, int],
    path: List[str]
) -> None:
    """
    Escribe el fichero de salida del laberinto.
    Args:
        filename: Nombre del fichero donde se escribe el resultado.
        hex_maze: Laberinto codificado en hexadecimal.
        entry: Coordenada de entrada del laberinto.
        exit_cell: Coordenada de salida del laberinto.
        path: Lista de letras con el camino mas corto.
    Returns:
        Ninguno.
    Raises:
        OSError: Si el fichero no se puede abrir o escribir.
    """

    with open(filename, 'w') as f:
        f.write(hex_maze + '\n')
        f.write('\n')
        f.write(f"{entry[0]},{entry[1]}\n")
        f.write(f"{exit_cell[0]},{exit_cell[1]}\n")
        f.write(''.join(path) + '\n')
