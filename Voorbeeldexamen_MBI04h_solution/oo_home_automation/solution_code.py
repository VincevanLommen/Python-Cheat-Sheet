from abc import ABC, abstractmethod

class Location:
    def __init__(self, room, floor):
        self.room = room
        self.floor = floor

class Device(ABC):
    def __init__(self, name, location, electricity_consumption):
        self.__name = name
        self.__location = location
        self.__electricity_consumption = electricity_consumption

    @property
    def name(self):
        return self.__name

    @property
    def location(self):
        return self.__location

    @property
    def electricity_consumption(self):
        return self.__electricity_consumption
    
    @property
    @abstractmethod
    def is_on(self):
        pass

    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass
    
    def __eq__(self, other):
        if not isinstance(other, Device):
            return NotImplemented
        return self.electricity_consumption == other.electricity_consumption
    
    def __lt__(self, other):
        if not isinstance(other, Device):
            return NotImplemented
        return self.electricity_consumption < other.electricity_consumption
    
    def __gt__(self, other):
        if not isinstance(other, Device):
            return NotImplemented
        return self.electricity_consumption > other.electricity_consumption

class Lamp(Device):
    def __init__(self, name, location, electricity_consumption):
        super().__init__(name, location, electricity_consumption)
        self.__brightness = 0

    @property
    def brightness(self):
        return self.__brightness
        
    @property
    def is_on(self):
        return self.__brightness > 0

    def turn_on(self):
        self.__brightness = 100
        
    def turn_off(self):
        self.__brightness = 0
    
class Heating(Device):
    def __init__(self, name, location, electricity_consumption):
        if not isinstance(location, Location):
            raise TypeError("Location must be an instance of Location class")
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        if name.strip() == "":
            raise ValueError("Name cannot be an empty string")
        if not isinstance(electricity_consumption, int):
            raise TypeError("Electricity consumption must be an integer")
        if electricity_consumption < 0:
            raise ValueError("Electricity consumption cannot be negative")     
        
        super().__init__(name, location, electricity_consumption)
        self.__temperature = 0
        self.__preferred_temperature = 20

    @property
    def temperature(self):
        return self.__temperature
        
    @property
    def preferred_temperature(self):
        return self.__preferred_temperature
    
    @preferred_temperature.setter
    def preferred_temperature(self, temperature):
        self.__preferred_temperature = temperature
        
    @property
    def is_on(self):
        return self.__temperature > 0
        
    def turn_on(self):
        self.__temperature = self.__preferred_temperature

    def turn_off(self):
        self.__temperature = 0
    
class WashingMachine(Device):
    def __init__(self, name, location, electricity_consumption):
        super().__init__(name, location, electricity_consumption)
        self.__is_on = False

    @property
    def is_on(self):
        return self.__is_on

    def turn_on(self):
        self.__is_on = True

    def turn_off(self):
        self.__is_on = False
    
class HomeAutomation:
    def __init__(self):
        self.__devices = []

    def add_device(self, device):
        self.__devices.append(device)

    def turn_on_all(self):
        for device in self.__devices:
            device.turn_on()

    def turn_off_all(self):
        for device in self.__devices:
            device.turn_off()
            
    def filter(self, condition):
        return [device for device in self.__devices if condition(device)]
    
    def filter_by_location(self, location):
        if not isinstance(location, Location):
            raise TypeError("Location must be an instance of Location class")
        return self.filter(lambda device: device.location == location)
    
    def filter_by_energy_consumption(self, energy_consumption):
        if not isinstance(energy_consumption, (int, float)):
            raise TypeError("Energy consumption must be a number")
        return self.filter(lambda device: device.electricity_consumption <= energy_consumption)
            
    def get_status(self):
        status = ""
        for device in self.__devices:
            status += f"{device.name} at {device.location.room} on floor {device.location.floor} is {'on' if device.is_on else 'off'}\n"
        return status
