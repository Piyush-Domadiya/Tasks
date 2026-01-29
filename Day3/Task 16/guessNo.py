#Write a number guessing game that generates a random number and asks the user to guess it.
import random
class GuessingGame:
    def __init__(self):
        self.secret_number = random.randint(1, 50)
        self.attempts = 0

    def play(self):
        while True:
            guess = int(input("Guess a number between 1 and 50: "))
            self.attempts += 1

            if guess == self.secret_number:
                print(f"Congratulations! You guessed the number in {self.attempts} attempts.")
                break
            elif guess < self.secret_number:
                print("Too low! Try again.")
            else:
                print("Too high! Try again.")
            if self.attempts >= 5:
                print(f"Sorry, you've used all your attempts. The number was {self.secret_number}.")
                break   

game = GuessingGame()
game.play()