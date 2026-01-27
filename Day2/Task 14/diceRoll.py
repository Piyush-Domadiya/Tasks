#Use the random module to simulate a dice roll.
import random
while True:
    roll = input("You want to roll the dice? (yes/no): ")
    if roll.lower() == 'yes':
        print("Rolling the dice...")
        print("The value is:", random.randint(1, 6))
    elif roll.lower() == 'no':
        print("Exiting the dice roller.")
        break
    else:
        print("Invalid input. Please enter 'yes' or 'no'.")