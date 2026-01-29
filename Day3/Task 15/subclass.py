#Create a subclass ElectricCar that inherits from Car and adds an additional battery_size attribute.
class Car:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

class ElectricCar(Car):
    def __init__(self, make, model, year, battery_size):
        super().__init__(make, model, year)
        self.battery_size = battery_size

#Create an object of the ElectricCar class
my_electric_car = ElectricCar("Tesla", "Model S", 2022, 100)
print(my_electric_car.make)          
print(my_electric_car.model)         
print(my_electric_car.year)          
print(my_electric_car.battery_size)  