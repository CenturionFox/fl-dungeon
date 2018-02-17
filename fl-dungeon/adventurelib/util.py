import adventurelib
import pkgutil

def isValidInt(value):
    """Checks if the input is a valid integer."""
    try:
        int(value)
        return True
    except ValueError and TypeError:
        return False

def clearConsole():
    """Clears the console output."""
    os.system('cls' if os.name == 'nt' else 'clear')
