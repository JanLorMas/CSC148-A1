"""Drivers for the simulation"""

from typing import Optional
from location import Location, manhattan_distance
from rider import Rider


class Driver:
    """A driver for a ride-sharing service.

    === Attributes ===
    id: A unique identifier for the driver.
    location: The current location of the driver.
    speed: The speed of the driver's car
    is_idle: True if the driver is idle and False otherwise.'
    destination: Possible destination for Driver
    """
    # Attribute Types
    id: str
    location: Location
    speed: int
    is_idle: bool
    destination: Optional[Location]

    def __init__(self, identifier: str, location: Location,
                 speed: int, destination: Optional[Location] = None) -> None:
        """Initialize a Driver.

        >>> d = Driver("Amaranth", Location(1,1), 1, Location(1,1))
        >>> d.destination.__str__()
        '(1,1)'
        """
        self.id = identifier
        self.location = location
        self.speed = speed
        self.is_idle = True
        self.destination = destination

    def __str__(self) -> str:
        """Return a string representation.

        >>> d = Driver("Amaranth", Location(1,1), 1)
        >>> d.__str__()
        'Amaranth'
        """
        return self.id

    def __eq__(self, other: object) -> bool:
        """Return True if self equals other, and false otherwise.

        >>> d = Driver("Amaranth", Location(1,1), 1)
        >>> d2 = Driver("Amaranth", Location(1,1), 1)
        >>> d3 = Driver("Bob", Location(1,1), 0)
        >>> d.__eq__(d2)
        True
        >>> d.__eq__(d3)
        False
        """
        A = (self.id == other.id)
        B = (self.location == other.location)
        C = (self.speed == other.speed)
        D = (self.is_idle == other.is_idle)
        return A and B and C and D

    def get_travel_time(self, destination: Location) -> int:
        """Return the time it will take to arrive at the destination,
        rounded to the nearest integer.
        >>> d = Driver("Amaranth", Location(5,5), 2)
        >>> d.get_travel_time(Location(9,7))
        3
        """
        m_distance = manhattan_distance(self.location, destination)
        return m_distance // self.speed

    def start_drive(self, location: Location) -> int:
        """Start driving to the location.
        Return the time that the drive will take.

        >>> d = Driver("Amaranth", Location(5,5), 2)
        >>> d.start_drive(Location(9,7))
        3
        """
        self.is_idle = False
        self.destination = location
        return self.get_travel_time(location)

    def end_drive(self) -> None:
        """End the drive and arrive at the destination.

        Precondition: self.destination is not None.

        """
        self.is_idle = True
        self.location = self.destination
        self.destination = None

    def start_ride(self, rider: Rider) -> int:
        """Start a ride and return the time the ride will take.

        >>> d = Driver("Amaranth", Location(5,5), 2)
        >>> d.start_ride(Rider("Bob", 0, Location(5,5), Location(9,7)))
        3
        """
        self.is_idle = False
        self.destination = rider.destination
        return self.get_travel_time(rider.destination)

    def end_ride(self) -> None:
        """End the current ride, and arrive at the rider's destination.

        Precondition: The driver has a rider.
        Precondition: self.destination is not None.

        """
        self.is_idle = True
        self.location = self.destination
        self.destination = None


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(
        config={'extra-imports': ['location', 'rider']})
