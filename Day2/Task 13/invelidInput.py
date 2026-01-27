#Write a program to handle invalid user input
while True:
    try:
        user_input = int(input("Please enter an integer: "))
        print(f"You entered: {user_input}")
        break
    except ValueError:
        print("Invalid input. Please enter a valid integer.")