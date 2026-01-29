#a simple project such as a calculator that can add, subtract, multiply, and divide numbers.
def add(x, y):
    return x + y
def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y==0:
        return "Error! Division by zero."
    else:
        return x / y

while True:
    num1=float(input("Enter first number: "))
    num2=float(input("Enter second number: "))
    print("Select operation.")
    print("1.Add \n2.Subtract \n3.Multiply \n4.Divide")
    choice=input("Enter choice(1/2/3/4): ")

    match choice:
        case '1':
            print(add(num1, num2))
        case '2':
            print(subtract(num1, num2))
        case '3':
            print(multiply(num1, num2))
        case '4':
            print(divide(num1, num2))
    
    ans=input("Do you want to perform another calculation? (yes/no): ")
    if ans.lower() != 'yes':
        break
    else:
        continue