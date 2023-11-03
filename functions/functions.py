def set_cache(cache: dict[str, any], key: str, value: any) -> None:
    """Sets a value in the cache with the given key.

    Args:
        cache (dict[str, any]): The cache to modify.
        key (str): The key/index of the cache.
        value (any): The value to set the cache.
    """
    cache[key] = value

def add(cache: dict[str, any], key: str, lhs: any, rhs: any) -> None:
    """Adds 2 values and assigns it to a key in the cache.

    Args:
        cache (dict[str, any]): The cache to modify.
        key (str): The key to store the result to.
        lhs (any): The left hand side of the addition.
        rhs (any): The right hand side of the addition.
    """
    cache[key] = lhs + rhs

def subtract(cache: dict[str, any], key: str, lhs: any, rhs: any) -> None:
    """Subtracts 2 values and assigns it to a key in the cache.

    Args:
        cache (dict[str, any]): The cache to modify.
        key (str): The key to store the result to.
        lhs (any): The left hand side of the subtraction.
        rhs (any): The right hand side of the subtraction.
    """
    cache[key] = lhs - rhs

def get_target_attribtue(cache: dict[str, any], key: str, target_index: int, target_key: str) -> None:
    """Gets a value stored in a target's cache.

    Gets a value stored in a target's cache.

    Args:
        cache (dict[str, any]): The cache to obtain the target from.
        key (str): The key to store the result to.
        target_index (int): The index of the desired target.
        target_key (str): The key that stores the desired data in the 
        target.
    """
    if target_index >= 0: cache[key] = cache['targets'][target_index].cache[target_key]

def compare(cache: dict[str, any], key: str, lhs: any, rhs: any, operator: str) -> bool:
    """Compares two values.

    Compares two values with the operators: > (greater than), 
    >= (greater than or equal to), = (equal to), <= (less than or
    equal to), < (less than), != (not equal to).

    Args:
        cache (dict[str, any]): The cache to store the data in.
        key (str): The key to store the result to.
        lhs (any): The left hand side of the comparison.
        rhs (any): The right hand side of the comparison.
        operator (str): The operation to perform.

    Returns:
        The boolean obtained from the comparison.
    """
    match operator:
        case '>':
            cache[key] = lhs > rhs
        case '>=':
            cache[key] = lhs >= rhs
        case '=':
            cache[key] = lhs == rhs
        case '<=':
            cache[key] = lhs <= rhs
        case '<':
            cache[key] = lhs < rhs
        case '!=':
            cache[key] = lhs != rhs

    return cache[key]

def log(cache: dict[str, any], format: str, **kwargs: dict[str, any]) -> None:
    """Prints the given format and keyword arguments to the console.

    Args:
        format (str): The string format.
        kwargs (dict[str, any]): The key word arguments to insert 
        into the format string.
    """
    print(f'[{cache["name"]} log]: {format.format(**kwargs)}')

FUNCTIONS = {
    'set cache': set_cache,
    'add': add,
    'subtract': subtract,
    'get target attribute': get_target_attribtue,
    'compare': compare,
    'log': log
}