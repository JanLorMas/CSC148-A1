"""Dispatcher for the simulation"""

from typing import Optional
from driver import Driver
from rider import Rider


class Dispatcher:
    """A dispatcher fulfills requests from riders and drivers for a
    ride-sharing service.

    When a rider requests a driver, the dispatcher assigns a driver to the
    rider. If no driver is available, the rider is placed on a waiting
    list for the next available driver. A rider that has not yet been
    picked up by a driver may cancel their request.

    When a driver requests a rider, the dispatcher assigns a rider from
    the waiting list to the driver. If there is no rider on the waiting list
    the dispatcher does nothing. Once a driver requests a rider, the driver
    is registered with the dispatcher, and will be used to fulfill future
    rider requests.

    === Attributes ===
    waiting_riders: A list of riders that are waiting for an available driver
    available_drivers: A list of drivers ready to
    """
    # Attribute Types
    waiting_riders: list
    available_drivers: list

    def __init__(self) -> None:
        """Initialize a Dispatcher.

        >>> di = Dispatcher()
        >>> di.waiting_riders
        []
        >>> di.available_drivers
        []
        """
        self.waiting_riders = []
        self.available_drivers = []

    def __str__(self) -> str:
        """Return a string representation.

        >>> di = Dispatcher()
        >>> di.waiting_riders
        []
        >>> di.available_drivers
        []
        >>> di.__str__()
        'Waiting list: [] Availble Drivers: []'
        """
        new_str = f'Waiting list: {self.waiting_riders}' \
                  f' Available Drivers: {self.available_drivers}'
        return new_str

    def request_driver(self, rider: Rider) -> Optional[Driver]:
        """Return a driver for the rider, or None if no driver is available.

        Add the rider to the waiting list if there is no available driver.

        """
        if not self.available_drivers:
            self.waiting_riders.append(rider)
            return None
        else:
            fastest_time = 9999999
            fastest_driver = None
            first_driver = True
            for driver in self.available_drivers:
                if first_driver:
                    fastest_driver = driver
                    fastest_time = driver.get_travel_time(rider.origin)
                    first_driver = False
                elif driver.get_travel_time(rider.origin) < fastest_time:
                    fastest_driver = driver
                    fastest_time = driver.get_travel_time(rider.origin)
            return fastest_driver

    def request_rider(self, driver: Driver) -> Optional[Rider]:
        """Return a rider for the driver, or None if no rider is available.

        If this is a new driver, register the driver for future rider requests.

        """
        if not self.waiting_riders:
            self.available_drivers.append(driver)
            return None
        else:
            rider = self.waiting_riders.pop(0)
            return rider

    def cancel_ride(self, rider: Rider) -> None:
        """Cancel the ride for rider.

        """
        rider.status = "cancelled"
        self.waiting_riders.remove(rider)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={'extra-imports': ['typing', 'driver', 'rider']})
