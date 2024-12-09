"""
The rider module contains the Rider class. It also contains
constants that represent the status of the rider.

=== Constants ===
WAITING: A constant used for the waiting rider status.
CANCELLED: A constant used for the cancelled rider status.
SATISFIED: A constant used for the satisfied rider status
"""

from location import Location

WAITING = "waiting"
CANCELLED = "cancelled"
SATISFIED = "satisfied"


class Rider:

    """A rider for a ride-sharing service.

    === Attributes ===
    id: The unique id of the rider
    patience: The number of time units that the rider will
        wait to be picked up before they cancel their trip
    origin: Starting location of the rider
    destination: Desired location of the rider
    status: Current status of the rider: "waiting", "cancelled",
        or "satisfied"

    """
    # Attribute Types
    id: str
    patience: int
    origin: Location
    destination: Location
    status: str

    def __init__(self, identifier: str, patience: int, origin: Location,
                 destination: Location) -> None:
        """Initialize a Rider.

        """
        self.id = identifier
        self.patience = patience
        self.origin = origin
        self.destination = destination
        self.status = WAITING


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={'extra-imports': ['location']})
