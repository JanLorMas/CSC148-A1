from location import Location
from rider import Rider
from driver import Driver
from dispatcher import Dispatcher
from event import Event, create_event_list, DriverRequest, RiderRequest
from simulation import Simulation


def test_rider() -> None:
    """
    Tests the initialization of a rider object from the events textfile.
    """
    origin = Location(3, 2)
    destination = Location(2, 3)
    curr_rider = Rider('Bisque', 5, origin, destination)
    assert str(curr_rider) == 'Bisque, (3, 2), (2, 3), 5'


def test_driver_init() -> None:
    """
    Tests the initialization of a driver object from the
    events textfile.
    """
    # Testing the initialization
    location = Location(3, 1)
    driver_1 = Driver('Crocus', location, 1)
    assert str(driver_1) == 'Crocus, (3, 1), 1, True'


def test_driver_eq() -> None:
    """
    Tests the equals method implemented in the Driver class
    """
    location = Location(3, 1)
    driver_1 = Driver('Crocus', location, 1)
    location_2 = Location(4, 2)
    driver_2 = Driver('Edelweiss', location_2, 1)
    driver_3 = Driver('Edelweiss', location, 1)
    assert (driver_1 == driver_2) is False
    assert (driver_3 == driver_2) is True


def test_driver_travel_time() -> None:
    """
    Tests the get_travel_time method implemented in the Driver class.
    Note that this method uses external methods to return the appropriate value
    """
    location_2 = Location(4, 2)
    driver_2 = Driver('Edelweiss', location_2, 1)
    origin = Location(2, 1)
    destination = Location(2, 5)
    rider = Rider('Fallow', 10, origin, destination)
    assert driver_2.get_travel_time(rider.destination) == 5


def test_driver_drive() -> None:
    """
    Tests the start_drive and end_drive methods in the Driver class;
    specifically testing the states of attributes after running the methods.
    """
    location_2 = Location(4, 2)
    driver_2 = Driver('Edelweiss', location_2, 1)
    origin = Location(2, 1)
    destination = Location(2, 5)
    rider = Rider('Fallow', 10, origin, destination)
    driver_2.start_drive(rider.origin)
    driver_2.end_drive()
    assert driver_2.location == rider.origin
    assert driver_2.is_idle is True


def test_driver_ride() -> None:
    """
    Tests the start_ride and end_rite methods in the Driver class, and checking
    the states of the involved attributes. The ride methods are assumed to
    occur without the rider cancelling here.
    """
    location_2 = Location(4, 2)
    driver_2 = Driver('Edelweiss', location_2, 1)
    origin = Location(2, 1)
    destination = Location(2, 5)
    rider = Rider('Fallow', 10, origin, destination)
    driver_2.start_ride(rider)
    driver_2.end_ride()
    assert driver_2.location == rider.destination
    assert driver_2.is_idle is True


def test_request_driver() -> None:
    # when driver list is empty
    dispatcher = Dispatcher()
    rider = Rider('Desert', 5, Location(5, 1), Location(4, 3))
    dispatcher.request_driver(rider)
    assert dispatcher.waiting_riders == [rider]

    # when driver is available for a rider
    dispatcher.drivers = [Driver('Foxglove', Location(3, 1), 1),
                          Driver('Edelweiss', Location(4, 2), 1),
                          Driver('Crocus', Location(5, 2), 1),
                          Driver('Amaranth', Location(1, 1), 1)]
    assert dispatcher.available_drivers == [1]
    assert dispatcher.request_driver(rider) == dispatcher.available_drivers[2]

    # when drivers are all available but are the same speed
    dispatcher.drivers = [Driver('Foxglove', Location(5, 2), 1),
                          Driver('Edelweiss', Location(5, 2), 1),
                          Driver('Crocus', Location(5, 2), 1),
                          Driver('Amaranth', Location(5, 2), 1)]
    assert dispatcher.request_driver(rider) == dispatcher.available_drivers[0]

    # when the fastest drivers speed is zero
    dispatcher.drivers = [Driver('Foxglove', Location(3, 1), 1),
                          Driver('Edelweiss', Location(5, 1), 1),
                          Driver('Crocus', Location(4, 2), 1),
                          Driver('Amaranth', Location(1, 1), 1)]
    assert dispatcher.request_driver(rider) == dispatcher.available_drivers[1]

    # when all drivers are unavailable but present
    dispatcher.drivers = [Driver('Foxglove', Location(3, 1), 1),
                          Driver('Edelweiss', Location(4, 2), 1),
                          Driver('Crocus', Location(5, 2), 1),
                          Driver('Amaranth', Location(1, 1), 1)]
    for driver in dispatcher.drivers:
        driver.is_idle = False
    dispatcher.request_driver(rider)
    assert dispatcher.waiting_riders == [rider, rider]  # Note that riders was not
    # emptied prior to running this test.


def test_request_rider() -> None:
    # When driver is not already registered and assigned to a rider
    dispatcher = Dispatcher()
    dispatcher.riders = [Rider('Cerise', 15, Location(4, 1), Location(1, 5)),
                         Rider('Desert', 5, Location(5, 1), Location(4, 3))]
    dispatcher.drivers = [Driver('Foxglove', Location(3, 1), 1),
                          Driver('Edelweiss', Location(4, 2), 1),
                          Driver('Crocus', Location(5, 2), 1)]
    unregistered_driver = Driver('Amaranth', Location(1, 1), 1)
    waiting_rider = dispatcher.riders[0]
    assert dispatcher.request_rider(unregistered_driver) == waiting_rider
    assert dispatcher.drivers == [Driver('Foxglove', Location(3, 1), 1),
                                  Driver('Edelweiss', Location(4, 2), 1),
                                  Driver('Crocus', Location(5, 2), 1),
                                  Driver('Amaranth', Location(1, 1), 1)]

    # When driver is already registered and assigned a rider
    dispatcher.drivers = [Driver('Foxglove', Location(3, 1), 1),
                          Driver('Edelweiss', Location(4, 2), 1),
                          Driver('Crocus', Location(5, 2), 1),
                          Driver('Amaranth', Location(1, 1), 1)]
    waiting_rider = dispatcher.riders[0]
    assert dispatcher.request_rider(dispatcher.drivers[3]) == waiting_rider

    # When driver is registered but no rider is available
    assert dispatcher.request_rider(dispatcher.drivers[1]) is None


def test_cancel_ride() -> None:
    # When rider is in the waiting list and cancels their ride
    dispatcher = Dispatcher()
    dispatcher.riders = [Rider('Cerise', 15, Location(4, 1), Location(1, 5)),
                         Rider('Desert', 5, Location(5, 1), Location(4, 3))]
    cancelled_rider = dispatcher.riders[0]
    dispatcher.cancel_ride(dispatcher.riders[0])
    assert cancelled_rider not in dispatcher.riders
    assert cancelled_rider.status == 'cancelled'

    # When rider is not in the waiting list
    dispatcher.riders = [Rider('Desert', 5, Location(5, 1), Location(4, 3))]
    random_rider = Rider('Cerise', 15, Location(4, 1), Location(1, 5))
    assert dispatcher.cancel_ride(random_rider) is None


def test_events_cancels():
    """Tests what happens if every rider cancels on the driver, and tests
    the report that follows alongside it. More information about the order of
    events and their timestamps can be found in the textfile.

    """
    import pytest

    events = create_event_list("my_events.txt")

    assert len(events) == 5
    sim = Simulation()
    report = sim.run(events)
    # print(sim._monitor._activities['driver'])
    assert len(report) == 3
    assert report['rider_wait_time'] == pytest.approx(6.66666667)
    assert report['driver_total_distance'] == pytest.approx(18.0)
    assert report['driver_ride_distance'] == pytest.approx(0)


def test_events_drivers():
    import pytest

    events = create_event_list("events_drivers.txt")

    assert len(events) == 6
    sim = Simulation()
    report = sim.run(events)
    # print('')
    # print(sim._monitor._activities['driver'])
    # print(sim._monitor._activities['rider'])
    assert len(report) == 3
    assert report['rider_wait_time'] == pytest.approx(7.75)
    assert report['driver_total_distance'] == pytest.approx(17.0)
    assert report['driver_ride_distance'] == pytest.approx(5.5)

def test_events_rider_requests():
    """ Tests the creation of the rider waiting list once more and tests
    rider cancellations alongside the behaviour of drivers as they drive to
    locations.

    """
    import pytest

    events = create_event_list("testingCopy")

    assert len(events) == 9
    sim = Simulation()
    report = sim.run(events)
    assert len(report) == 3
    print(report)


if __name__ == '__main__':
    import pytest

    # Change the filename here to suit your testcases file.
    pytest.main(['a1_tests.py'])
