#a simple project such as a calculator that can add, subtract, multiply, and divide numbers.
import logging
logging.basicConfig(
    filename="calculator.log",
    level=logging.INFO , format="%(asctime)s - %(levelname)s - %(message)s")

def add(x, y):
    logging.info(f"called add() with arguments {x} and {y} , Result: {x + y}")
    return x + y
def subtract(x, y):
    logging.info(f"called subtract() with arguments {x} and {y} , Result: {x - y}")
    return x - y

def multiply(x, y):
    logging.info(f"called multiply() with arguments {x} and {y} , Result: {x * y}")
    return x * y

def divide(x, y):
    try:
        logging.info(f"called divide() with arguments {x} and {y} , Result: {x / y}")
        result = x / y
    except ZeroDivisionError:
        logging.exception(f"error Division by zero ")
        return "Error! Division by zero."
    return result

logging.info(f"Calculator started.")
while True:
    try:
        num1=float(input("Enter first number: "))
        num2=float(input("Enter second number: "))
    except ValueError as e:
        logging.warning(e)
        print("Invalid input. Please enter numeric values.")
        continue
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
        case _:
            logging.warning(f"Invalid choice {choice}")
            print("Invalid input")
    
    ans=input("Do you want to perform another calculation? (yes/no): ")

    if ans.lower() != 'yes':
        logging.info("User exiting the calculator.")
        break
    