#Create a class called Car with attributes like make, model, and year.
class Car:
  def __init__(self, make, model, year):
    self.make = make
    self.model = model
    self.year = year

#Create an object of the Car class
my_car = Car("Toyota", "Camry", 2020)
print(my_car.make)   # Output: Toyota
print(my_car.model)  # Output: Camry    
print(my_car.year)   # Output: 2020