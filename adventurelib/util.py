
def isValidInt(value):
    """Checks if the input is a valid integer."""
    try:
        int(value)
        return True
    except ValueError and TypeError:
        return False

