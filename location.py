"""Locations for the simulation"""

from __future__ import annotations


class Location:
    """A two-dimensional location.

    === Attributes ===
    row: the number of blocks the location is from
        the left of the grid.
    column: the number of blocks the location is
        from the bottom edge of the grid.

    === Representation Invariants ===
    - The row and column attributes must be non-negative
    integers.

    """
    # Attribute types
    row: int
    column: int

    def __init__(self, row: int, column: int) -> None:
        """Initialize a location.

        Precondition: row >= 0 and column >= 0

        >>> l = Location(0,0)
        >>> l.row
        0
        >>> l.column
        0
        """
        self.row = row
        self.column = column

    def __str__(self) -> str:
        """Return a string representation.

        >>> l = Location(0,0)
        >>> l.__str__()
        '0,0'
        """
        return f'({self.row},{self.column})'

    def __eq__(self, other: Location) -> bool:
        """Return True if self equals other, and false otherwise.

        >>> l = Location(0,0)
        >>> l2 = Location(0,0)
        >>> l3 = Location(0,2)
        >>> l.__eq__(l2)
        True
        >>> l.__eq__(l3)
        False
        """
        return (self.row == other.row) and (self.column == other.column)


def manhattan_distance(origin: Location, destination: Location) -> int:
    """Return the Manhattan distance between the origin and the destination.

    >>> l = Location(5,5)
    >>> l2 = Location(9,7)
    >>> manhattan_distance(l, l2)
    6
    """
    row_value = abs(origin.row - destination.row)
    column_value = abs(origin.column - destination.column)
    return row_value + column_value


def deserialize_location(location_str: str) -> Location:
    """Deserialize a location.

    location_str: A location in the format 'row,col'

    >>> l = deserialize_location('0,0')
    >>> l.row
    0
    >>> l.column
    0
    """
    coordinate = location_str.partition(',')
    return Location(int(coordinate[0]), int(coordinate[2]))


if __name__ == '__main__':
    import python_ta

    python_ta.check_all()
