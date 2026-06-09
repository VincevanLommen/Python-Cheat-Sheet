import pytest
from solution_code import Heating, Location

# write tests for the `Heating` class constructor and include the following:
#  - at least one succesful creation of a `Heating` object
#  - test all possible exceptions using a parameterized test.

@pytest.mark.parametrize(
    "name, location, electricity_consumption",
    [
        ("Heater", Location("Living Room", 1), 1500),
        ("Radiator", Location("Bedroom", 2), 800),
    ],
)
def test_heating_initialization(name, location, electricity_consumption):
    h = Heating(name, location, electricity_consumption)
    assert h.name == name
    assert h.location == location
    assert h.electricity_consumption == electricity_consumption

@pytest.mark.parametrize(
    "name, location, electricity_consumption, expected_exception",
    [
        (123, Location("Laundry Room", 1), 500, TypeError),
        ("Heater", "Not a Location", 500, TypeError),
        ("Heater", Location("Laundry Room", 1), "500", TypeError),
        ("", Location("Laundry Room", 1), 500, ValueError),
        ("Heater", Location("Laundry Room", 1), -100, ValueError),
    ],
)
def test_heating_exceptions(name, location, electricity_consumption, expected_exception):
    with pytest.raises(expected_exception):
        Heating(name, location, electricity_consumption)