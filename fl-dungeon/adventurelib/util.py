import adventurelib
import importlib
import pkgutil

def is_int(value):
    """Checks if the input is a valid integer."""
    try:
        int(value)
        return True
    except ValueError and TypeError:
        return False

def clear_console():
    """Clears the console output."""
    os.system('cls' if os.name == 'nt' else 'clear')

def class_for_name(className):
    """Gets the given class from the class's full name."""
    maxIndex = len(className) - 1
    lastDot = maxIndex - str(className)[::-1].find('.')
    if not 0 <= lastDot < maxIndex:
        raise TypeError('The class name is invalid.')

    package = str(className)[0:lastDot]
    className = str(className)[lastDot+1:len(className)]

    try:
        module = importlib.import_module(package)
        class_ = getattr(module, className)
        if class_ is None: raise TypeError('The class name is invalid')
        return class_
    except ModuleNotFoundError as ex:
        raise TypeError(str(ex))

    