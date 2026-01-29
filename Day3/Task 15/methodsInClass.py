#Write methods in the class to display the car’s details.
class Car:
  def __init__(self, make, model, year):
    self.make = make
    self.model = model
    self.year = year

  def display_details(self):
    print(f"Make: {self.make}, Model: {self.model}, Year: {self.year}")

#Create an object of the Car class
my_car = Car("Tata", "Nexon", 2020)
my_car.display_details()  # Output: Make: Tata, Model: Nexon, Year: 2020

