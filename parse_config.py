"""
Modulo de lectura y validacion del fichero de configuracion del
proyecto A-Maze-ing.
Args:
    Ninguno.
Returns:
    Ninguno.
Raises:
    Ninguna.
"""
import os


INT32_MAX = 2_147_483_647
INT32_MIN = -2_147_483_648


class ConfigError(Exception):
    """
    Excepcion para los errores del fichero de configuracion.
    Args:
        Ninguno.
    Returns:
        Ninguno.
    Raises:
        Ninguna.
    """

    pass


def parse_config(file_route: str) -> dict:
    """
    Analiza y valida el fichero de configuracion del laberinto.
    Args:
        file_route: Ruta del fichero de configuracion.
    Returns:
        Diccionario con los valores de configuracion validados y tipados.
    Raises:
        ConfigError: Si el fichero falta, esta mal formado o tiene
            valores invalidos.
    """
    config_raw = read_config(file_route)
    validate_keys(config_raw)
    config_typed = typing_validating(config_raw)
    return config_typed


def read_config(ruta_config: str) -> dict:
    """
    Lee los pares clave=valor en bruto del fichero de configuracion.
    Args:
        ruta_config: Ruta del fichero de configuracion.
    Returns:
        Diccionario con los pares clave-valor en formato texto.
    Raises:
        ConfigError: Si el fichero no se encuentra o tiene errores
            de sintaxis.
    """
    config_raw: dict = {}
    try:
        with open(ruta_config, "r") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' not in line:
                    raise ConfigError(f"Invalid line (missing '='): '{line}'")
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                if not key or not value:
                    raise ConfigError(
                        f"Key or value is empty in line: '{line}'"
                    )
                if key in config_raw:
                    raise ConfigError(f"Duplicated key: '{key}'")
                config_raw[key] = value
    except FileNotFoundError:
        raise ConfigError(f"Config file not found: '{ruta_config}'")
    return config_raw


def validate_keys(data: dict) -> None:
    """
    Comprueba que estan presentes todas las claves obligatorias.
    Args:
        data: Diccionario de configuracion en bruto.
    Returns:
        Ninguno.
    Raises:
        ConfigError: Si falta alguna clave obligatoria.
    """
    required_keys = {'WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE',
                     'PERFECT'}
    for key in required_keys:
        if key not in data:
            raise ConfigError(f"Mandatory key missing: '{key}'")


def typing_validating(data: dict) -> dict:
    """
    Convierte y valida los valores de configuracion en bruto.
    Args:
        data: Diccionario de configuracion en formato texto.
    Returns:
        Diccionario de configuracion tipado y listo para usar.
    Raises:
        ConfigError: Si algun valor falla la validacion de tipo o rango.
    """
    validate_keys(data)
    try:
        width = int(data['WIDTH'])
        height = int(data['HEIGHT'])
    except ValueError:
        raise ConfigError("WIDTH and HEIGHT must be integers.")

    if width <= 0 or height <= 0:
        raise ConfigError("WIDTH and HEIGHT must be positive integers.")

    if width > INT32_MAX or height > INT32_MAX:
        raise ConfigError(
            f"WIDTH and HEIGHT cannot exceed INT_MAX ({INT32_MAX})"
        )

    entry = parse_coordinates(data['ENTRY'], width, height)
    exit_coords = parse_coordinates(data['EXIT'], width, height)

    if entry == exit_coords:
        raise ConfigError("ENTRY and EXIT cannot be the same cell.")

    is_perfect = parse_bool(data['PERFECT'])
    output_file = validate_output_file(data['OUTPUT_FILE'])

    seed: int | None = None
    if 'SEED' in data:
        try:
            seed = int(data['SEED'])
        except ValueError:
            raise ConfigError("SEED must be an integer.")
        if seed < INT32_MAX or seed > INT32_MAX:
            raise ConfigError(
                f"SEED must be within 32-bit signed integer limits "
                f"({INT32_MIN} to ({INT32_MAX})."
            )

    algorithm = data.get('ALGORITHM', 'iterative').lower()
    if algorithm not in ('iterative', 'recursive'):
        raise ConfigError(
            f"ALGORITHM must be 'iterative' or 'recursive', got '{algorithm}'"
        )

    return {
        "width": width,
        "height": height,
        "entry": entry,
        "exit": exit_coords,
        "perfect": is_perfect,
        "output_file": output_file,
        "seed": seed,
        "algorithm": algorithm,
    }


def validate_output_file(filename: str) -> str:
    """
    Comprueba que OUTPUT_FILE es un nombre de fichero simple.
    Args:
        filename: Valor bruto de OUTPUT_FILE en la configuracion.
    Returns:
        Nombre de fichero validado.
    Raises:
        ConfigError: Si el nombre contiene separadores de ruta o es
            un componente especial como '.' o '..'.
    """
    if os.path.basename(filename) != filename:
        raise ConfigError(
            f"OUTPUT_FILE must be a plain filename, not a path: '{filename}'"
        )
    if filename in ('.', '..'):
        raise ConfigError(f"Invalid OUTPUT_FILE: '{filename}'.")
    if not filename.strip():
        raise ConfigError("OUTPUT_FILE cannot be blank.")
    return filename


def parse_coordinates(coords_str: str, max_width: int,
                      max_height: int) -> tuple:
    """
    Analiza y valida una cadena de coordenadas con formato 'x,y'.
    Args:
        coords_str: Cadena de coordenadas en bruto.
        max_width: Limite del ancho del laberinto (exclusivo).
        max_height: Limite del alto del laberinto (exclusivo).
    Returns:
        Tupla de enteros (x, y).
    Raises:
        ConfigError: Si el formato es invalido o las coordenadas
            quedan fuera de rango.
    """
    if ',' not in coords_str:
        raise ConfigError(
            f"Invalid coordinate format (expected 'x,y'): '{coords_str}'"
        )
    parts = coords_str.split(',')
    if len(parts) != 2:
        raise ConfigError(
            f"Coordinates must have exactly two values: '{coords_str}'"
        )
    try:
        x = int(parts[0].strip())
        y = int(parts[1].strip())
    except ValueError:
        raise ConfigError(
            f"Coordinate values must be integers: '{coords_str}'"
        )
    if not (0 <= x < max_width) or not (0 <= y < max_height):
        raise ConfigError(
            f"Coordinates ({x},{y}) are out of maze bounds "
            f"({max_width}x{max_height})."
        )
    return (x, y)


def parse_bool(value: str) -> bool:
    """
    Analiza un valor booleano expresado como texto.
    Args:
        value: Cadena en bruto (por ejemplo 'true', 'false', '1', '0').
    Returns:
        Valor booleano correspondiente.
    Raises:
        ConfigError: Si el valor no se puede interpretar como booleano.
    """
    lower = value.lower()
    if lower in ("true", "1", "yes"):
        return True
    if lower in ("false", "0", "no"):
        return False
    raise ConfigError(f"Invalid boolean value: '{value}'")
