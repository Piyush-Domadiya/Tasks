#Create a class representing a simple Bank Account.
from random import choice


class Bank:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited {amount}. New balance is {self.balance}.")
    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds.")
            
        else:
            self.balance -= amount
            print(f"Withdrew {amount}. New balance is {self.balance}.")
#Create an object of the Bank class
my_account = Bank("John Doe", 1000)
print(f"Hello {my_account.name}")  
print(f"Your Current Balance is: {my_account.balance}")
input1="y"
while input1=="y": 
    choice=input("You want to deposit or withdraw amount?(w/d): ")
    if choice == "d":
        value=int(input("Enter the amount you want to deposit: "))
        my_account.deposit(value)
    elif choice == "w":
        value=int(input("Enter the amount you want to withdraw: "))
        my_account.withdraw(value)
    input1=input("Do you want to continue? (y/n): ")
        
    

print(f"Your Current Balance is: {my_account.balance}")    
     
    

