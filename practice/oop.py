""" class MyClass:
  x = 5
  #def __init__(self, name, age):
  def __init__(self, name, age=18):
    self.name = name
    self.age = age

  def myfunc(self):
    print("Hello my name is " + self.name)

p1 = MyClass("Krishna")
p2 = MyClass("Ram", 25) """
"""print(p1.name)
print(p1.age)
print(p2.name)
print(p2.age)"""
#using self keyword accessing the class method
#p1.myfunc() 
#p2.myfunc()

#print(p1.x) 

#del p1
#print(p1) 

#Class Properties
class Car:
  def __init__(self, brand, model):
    self.brand = brand
    self.model = model
  def __str__(self): 
    return f"{self.brand} ({self.model})"

car1 = Car("Tata", "Nexon")
print(car1.brand)  # Accessing the brand property
print(car1.model)  # Accessing the model property
car1.brand = "Honda"   # Modifying the brand property
car1.model = "City" # Modifying the model property


print(car1) # Using the __str__ method to print the object
