# Change the import to student to test your code
from solution_code import *

# Create locations
living_room = Location("Living Room", 1)
kitchen = Location("Kitchen", 1)
bathroom = Location("Bathroom", 2)

# Lamp usage
lamp = Lamp("Desk Lamp", living_room, 10)
print(f"Lamp name: {lamp.name}")
print(f"Lamp location: {lamp.location.room}, Floor: {lamp.location.floor}")
print(f"Lamp electricity consumption: {lamp.electricity_consumption}")
print(f"Lamp brightness: {lamp.brightness}")
print(f"Lamp is on? {lamp.is_on}")
lamp.turn_on()
print(f"Lamp turned on. Brightness: {lamp.brightness}, Is on? {lamp.is_on}")
lamp.turn_off()
print(f"Lamp turned off. Brightness: {lamp.brightness}, Is on? {lamp.is_on}")

# expected output:

# Lamp name: Desk Lamp
# Lamp location: Living Room, Floor: 1
# Lamp electricity consumption: 10
# Lamp brightness: 0
# Lamp is on? False
# Lamp turned on. Brightness: 100, Is on? True
# Lamp turned off. Brightness: 0, Is on? False

print("-" * 40)

# Heating usage
heating = Heating("Main Heater", kitchen, 2000)
print(f"Heating name: {heating.name}")
print(f"Heating location: {heating.location.room}, Floor: {heating.location.floor}")
print(f"Heating electricity consumption: {heating.electricity_consumption}")
print(f"Heating temperature: {heating.temperature}")
print(f"Heating preferred temperature: {heating.preferred_temperature}")
print(f"Heating is on? {heating.is_on}")
heating.turn_on()
print(f"Heating turned on. Temperature: {heating.temperature}, Is on? {heating.is_on}")
heating.turn_off()
print(f"Heating turned off. Temperature: {heating.temperature}, Is on? {heating.is_on}")
heating.preferred_temperature = 22
print(f"Heating preferred temperature set to: {heating.preferred_temperature}")

# expected output:

# Heating name: Main Heater
# Heating location: Kitchen, Floor: 1
# Heating electricity consumption: 2000
# Heating temperature: 0
# Heating preferred temperature: 20
# Heating is on? False
# Heating turned on. Temperature: 20, Is on? True
# Heating turned off. Temperature: 0, Is on? False
# Heating preferred temperature set to: 22

print("-" * 40)

# WashingMachine usage
washer = WashingMachine("Washer 3000", bathroom, 1500)
print(f"WashingMachine name: {washer.name}")
print(f"WashingMachine location: {washer.location.room}, Floor: {washer.location.floor}")
print(f"WashingMachine electricity consumption: {washer.electricity_consumption}")
print(f"WashingMachine is on? {washer.is_on}")
washer.turn_on()
print(f"WashingMachine turned on. Is on? {washer.is_on}")
washer.turn_off()
print(f"WashingMachine turned off. Is on? {washer.is_on}")

# expected output:

# WashingMachine name: Washer 3000
# WashingMachine location: Bathroom, Floor: 2
# WashingMachine electricity consumption: 1500
# WashingMachine is on? False
# WashingMachine turned on. Is on? True
# WashingMachine turned off. Is on? False