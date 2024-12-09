"""Simulation Events

This file should contain all of the classes necessary to model the different
kinds of events in the simulation.
"""
from __future__ import annotations
from typing import List
from rider import Rider, WAITING, CANCELLED, SATISFIED
from dispatcher import Dispatcher
from driver import Driver
from location import deserialize_location
from monitor import Monitor, RIDER, DRIVER, REQUEST, CANCEL, PICKUP, DROPOFF


class Event:
    """An event.

    Events have an ordering that is based on the event timestamp: Events with
    older timestamps are less than those with newer timestamps.

    This class is abstract; subclasses must implement do().

    You may, if you wish, change the API of this class to add
    extra public methods or attributes. Make sure that anything
    you add makes sense for ALL events, and not just a particular
    event type.

    Document any such changes carefully!

    === Attributes ===
    timestamp: A timestamp for this event.
    """

    timestamp: int

    def __init__(self, timestamp: int) -> None:
        """Initialize an Event with a given timestamp.

        Precondition: timestamp must be a non-negative integer.

        >>> Event(7).timestamp
        7
        """
        self.timestamp = timestamp

    # The following six 'magic methods' are overridden to allow for easy
    # comparison of Event instances. All comparisons simply perform the
    # same comparison on the 'timestamp' attribute of the two events.
    def __eq__(self, other: Event) -> bool:
        """Return True iff this Event is equal to <other>.

        Two events are equal iff they have the same timestamp.

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first == second
        False
        >>> second.timestamp = first.timestamp
        >>> first == second
        True
        """
        return self.timestamp == other.timestamp

    def __ne__(self, other: Event) -> bool:
        """Return True iff this Event is not equal to <other>.

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first != second
        True
        >>> second.timestamp = first.timestamp
        >>> first != second
        False
        """
        return not self == other

    def __lt__(self, other: Event) -> bool:
        """Return True iff this Event is less than <other>.

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first < second
        True
        >>> second < first
        False
        """
        return self.timestamp < other.timestamp

    def __le__(self, other: Event) -> bool:
        """Return True iff this Event is less than or equal to <other>.

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first <= first
        True
        >>> first <= second
        True
        >>> second <= first
        False
        """
        return self.timestamp <= other.timestamp

    def __gt__(self, other: Event) -> bool:
        """Return True iff this Event is greater than <other>.

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first > second
        False
        >>> second > first
        True
        """
        return not self <= other

    def __ge__(self, other: Event) -> bool:
        """Return True iff this Event is greater than or equal to <other>.

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first >= first
        True
        >>> first >= second
        False
        >>> second >= first
        True
        """
        return not self < other

    def __str__(self) -> str:
        """Return a string representation of this event.

        """
        raise NotImplementedError("Implemented in a subclass")

    def do(self, dispatcher: Dispatcher, monitor: Monitor) -> List[Event]:
        """Do this Event.

        Update the state of the simulation, using the dispatcher, and any
        attributes according to the meaning of the event.

        Notify the monitor of any activities that have occurred during the
        event.

        Return a list of new events spawned by this event (making sure the
        timestamps are correct).

        Note: the "business logic" of what actually happens should not be
        handled in any Event classes.

        """
        raise NotImplementedError("Implemented in a subclass")


class RiderRequest(Event):
    """A rider requests a driver.

    === Attributes ===
    rider: The rider.
    """

    rider: Rider

    def __init__(self, timestamp: int, rider: Rider) -> None:
        """Initialize a RiderRequest event.

        """
        super().__init__(timestamp)
        self.rider = rider

    def do(self, dispatcher: Dispatcher, monitor: Monitor) -> List[Event]:
        """Assign the rider to a driver or add the rider to a waiting list.
        If the rider is assigned to a driver, the driver starts driving to
        the rider.

        Return a Cancellation event. If the rider is assigned to a driver,
        also return a Pickup event.

        """
        monitor.notify(self.timestamp, RIDER, REQUEST,
                       self.rider.id, self.rider.origin)

        events = []
        driver = dispatcher.request_driver(self.rider)
        if driver is not None:
            travel_time = driver.start_drive(self.rider.origin)
            events.append(Pickup(self.timestamp + travel_time,
                                 self.rider, driver))
        events.append(Cancellation(self.timestamp + self.rider.patience,
                                   self.rider))
        return events

    def __str__(self) -> str:
        """Return a string representation of this event.

        """
        return f"({self.timestamp}) -- ({self.rider.id}): Request a driver"


class DriverRequest(Event):
    """A driver requests a rider.

    === Attributes ===
    driver: The driver.
    """

    driver: Driver

    def __init__(self, timestamp: int, driver: Driver) -> None:
        """Initialize a DriverRequest event.

        """
        super().__init__(timestamp)
        self.driver = driver

    def do(self, dispatcher: Dispatcher, monitor: Monitor) -> List[Event]:
        """Register the driver, if this is the first request, and
        assign a rider to the driver, if one is available.

        If a rider is available, return a Pickup event.

        """
        # Notify the monitor about the request.

        # Request a rider from the dispatcher.
        # If there is one available, the driver starts driving towards the
        # rider, and the method returns a Pickup event for when the driver
        # arrives at the riders location.
        monitor.notify(self.timestamp, DRIVER, REQUEST,
                       self.driver.id, self.driver.location)

        events = []
        requesting = dispatcher.request_rider(self.driver)
        if requesting is not None:
            travel_time = self.driver.start_drive(requesting.origin)
            events.append(Pickup(self.timestamp + travel_time,
                                 requesting, self.driver))
        return events

    def __str__(self) -> str:
        """Return a string representation of this event.

        """
        return f"({self.timestamp}) -- ({self.driver.id}): Request a rider"


class Cancellation(Event):
    """A rider cancels their ride request.

    === Attributes ===
    rider: The Rider.
    """
    rider: Rider

    def __init__(self, timestamp: int, rider: Rider) -> None:
        """Initialize a DriverRequest event.

        """
        super().__init__(timestamp)
        self.rider = rider

    def __str__(self) -> str:
        """Return a string representation of this event.

        """
        return f"({self.timestamp}) -- ({self.rider.id}): Cancel a rider"

    def do(self, dispatcher: Dispatcher, monitor: Monitor) -> List[Event]:
        """Changes a waiting rider to a cancelled rider
        """
        monitor.notify(self.timestamp, RIDER, CANCEL,
                       self.rider.id, self.rider.origin)

        self.rider.status = CANCELLED
        return []


class Pickup(Event):
    """A driver picks up their assigned rider

    === Attributes ===
    rider: The Rider.
    driver: The Driver.
    """
    rider: Rider
    driver: Driver

    def __init__(self, timestamp: int, rider: Rider, driver: Driver) -> None:
        """Initialize a Pickup event.

        """
        super().__init__(timestamp)
        self.rider = rider
        self.driver = driver

    def __str__(self) -> str:
        """Return a string representation of this event.

        """
        return f"({self.timestamp}) -- ({self.driver.id}) " \
               f"-- ({self.rider.id}): Driver picks up rider"

    def do(self, dispatcher: Dispatcher, monitor: Monitor) -> List[Event]:
        """Driver starts driving towards destination
        """
        monitor.notify(self.timestamp, DRIVER, PICKUP,
                       self.driver.id, self.rider.origin)

        events = []
        self.driver.location = self.rider.origin
        if self.rider.status == WAITING:
            travel_time = self.driver.start_ride(self.rider)
            monitor.notify(self.timestamp, RIDER, PICKUP,
                           self.rider.id, self.rider.origin)
            events.append(Dropoff(travel_time + self.timestamp,
                                  self.rider, self.driver))
            self.rider.status = SATISFIED
        elif self.rider.status == CANCELLED:
            events.append(DriverRequest(self.timestamp, self.driver))
            self.driver.destination = None
        return events


class Dropoff(Event):
    """A driver drops off their assigned rider

    === Attributes ===
    rider: The Rider.
    driver: The Driver.
    """
    rider: Rider
    driver: Driver

    def __init__(self, timestamp: int, rider: Rider, driver: Driver) -> None:
        """Initialize a Dropoff event.

        """
        super().__init__(timestamp)
        self.rider = rider
        self.driver = driver

    def __str__(self) -> str:
        """Return a string representation of this event.

        """
        return f"{self.timestamp} -- {self.driver.id} -- " \
               f"{self.rider.id}: Driver drops off rider"

    def do(self, dispatcher: Dispatcher, monitor: Monitor) -> List[Event]:
        """Driver starts driving towards destination
        """
        monitor.notify(self.timestamp, DRIVER, DROPOFF,
                       self.driver.id, self.rider.destination)

        events = []
        self.driver.location = self.rider.destination
        events.append(DriverRequest(self.timestamp, self.driver))
        self.driver.destination = None
        return events


def create_event_list(filename: str) -> List[Event]:
    """Return a list of Events based on raw list of events in <filename>.

    Precondition: the file stored at <filename> is in the format specified
    by the assignment handout.

    filename: The name of a file that contains the list of events.
    """
    events = []
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                # Skip lines that are blank or start with #.
                continue

            # Create a list of words in the line, e.g.
            # ['10', 'RiderRequest', 'Cerise', '4,2', '1,5', '15'].
            # Note that these are strings, and you'll need to convert some
            # of them to a different type.
            tokens = line.split()
            timestamp = int(tokens[0])
            event_type = tokens[1]
            event = None

            # HINT: Use Location.deserialize to convert the location string to
            # a location.

            if event_type == "DriverRequest":
                # Create a DriverRequest event.
                location = deserialize_location(tokens[3])
                driver = Driver(tokens[2], location, int(tokens[4]))
                event = DriverRequest(timestamp, driver)
            elif event_type == "RiderRequest":
                # Create a RiderRequest event.
                identifier = tokens[2]
                patience = int(tokens[5])
                origin = deserialize_location(tokens[3])
                destination = deserialize_location(tokens[4])
                rider = Rider(identifier, patience, origin, destination)
                event = RiderRequest(timestamp, rider)
            events.append(event)
    return events


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(
        config={
            'allowed-io': ['create_event_list'],
            'extra-imports': ['rider', 'dispatcher', 'driver',
                              'location', 'monitor']})
