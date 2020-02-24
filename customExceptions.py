"""
    Exception for when input is
    - in the wrong type or out of bound
    - too big or small for the ship
    - already mentioned before
"""
class InvalidEntry(Exception):
    pass


class InvalidSize(Exception):
    pass


class AlreadyTaken(Exception):
    pass
