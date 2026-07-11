"""Configuration file parser for the A-Maze-ing project."""
import os


class ConfigError(Exception):
    """Custom exception for configuration file errors."""

    pass


def parse_config(file_route: str) -> dict:
    """Parse and validate a maze configuration file.

    Args:
        file_route: Path to the configuration file.

    Returns:
        A dict with validated and typed configuration values.

    Raises:
        ConfigError: If the file is missing, malformed, or has invalid values.
    """
    config_raw = read_config(file_route)
    validate_keys(config_raw)
    config_typed = typing_validating(config_raw)
    return config_typed


def read_config(ruta_config: str) -> dict:
    """Read raw key=value pairs from a config file.

    Args:
        ruta_config: Path to the configuration file.

    Returns:
        A dict of raw string key-value pairs.

    Raises:
        ConfigError: If the file cannot be found or has syntax errors.
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
    """Ensure all mandatory keys are present in the raw config dict.

    Args:
        data: Raw config dict to validate.

    Raises:
        ConfigError: If any mandatory key is missing.
    """
    required_keys = {'WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE',
                     'PERFECT'}
    for key in required_keys:
        if key not in data:
            raise ConfigError(f"Mandatory key missing: '{key}'")


def typing_validating(data: dict) -> dict:
    """Convert and validate raw config values to their proper types.

    Args:
        data: Raw string config dict.

    Returns:
        A typed config dict ready for use.

    Raises:
        ConfigError: If any value fails type or range validation.
    """
    validate_keys(data)
    try:
        width = int(data['WIDTH'])
        height = int(data['HEIGHT'])
    except ValueError:
        raise ConfigError("WIDTH and HEIGHT must be integers.")

    if width <= 0 or height <= 0:
        raise ConfigError("WIDTH and HEIGHT must be positive integers.")

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
    """Ensure OUTPUT_FILE is a plain filename, not a path.

    Args:
        filename: The raw OUTPUT_FILE value from the config.

    Returns:
        The validated filename.

    Raises:
        ConfigError: If the filename contains path separators or is
            a special path component like '.' or '..'.
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
    """Parse and validate a coordinate string of the form 'x,y'.

    Args:
        coords_str: The raw coordinate string.
        max_width: Maze width bound (exclusive).
        max_height: Maze height bound (exclusive).

    Returns:
        A (x, y) integer tuple.

    Raises:
        ConfigError: If the format is invalid or coordinates are out of bounds.
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
    """Parse a boolean-like string value.

    Args:
        value: The raw string (e.g. 'true', 'false', '1', '0').

    Returns:
        The corresponding bool.

    Raises:
        ConfigError: If the value cannot be interpreted as a boolean.
    """
    lower = value.lower()
    if lower in ("true", "1", "yes"):
        return True
    if lower in ("false", "0", "no"):
        return False
    raise ConfigError(f"Invalid boolean value: '{value}'")
