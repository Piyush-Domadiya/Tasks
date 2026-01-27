a=int(input("Enter Number 1: "))
b=int(input("Enter Number 2: "))
try:
    result=a/b
    print("Result is:",result)
except ZeroDivisionError:
    print("Error: Division by zero is not allowed.")