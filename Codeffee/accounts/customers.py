import json
import os
import time
import sys
from random import randint
from config import CUSTOMER_MENU
from accounts.account import Account

class Customer:
    def __init__(self, filename="users.json", account = None):
        self.filename = filename
        self.account = account


        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as file:
                json.dump([], file)


    def load_users(self):
        with open(self.filename, 'r') as file:
            return json.load(file)

    def save_users(self, users):
        with open(self.filename, 'w') as file:
            return json.dump(users, file, indent=4)
        
    def get_fullname(self, email):
        users = self.load_users()
        for user in users:
            if user["email"] == email:
                return user["fullname"]
        return None

    # sign in
    def signin(self, fullname, email, password):
        users = self.load_users()
        for user in users:
            if user["email"] == email:
                print("An account already exists with this email")
                return False
            
        new_user = {
            "fullname": fullname,
            "email": email,
            "password": password,
            "balance": randint(10,50),
            "isAdmin": False
        }

        users.append(new_user)
        self.save_users(users)
        
        print("\033[92mRegistration completed successfully\033[0m")
        return True

    # login
    def login(self, email, password):
        users = self.load_users()
        for user in users:
            if user["email"] == email and user["password"] == password:
                print(f"Welcome \033[34m{user["fullname"]}\033[0m")
                print(f"\033[1;33mYour balance is {user["balance"]} AZN\033[0m ")
                return True
            
        print("Email or password is incorrect")
        return False
    
    def add_balance(self, user:dict, needed_amount:float):
        user_balance = user.get("balance", 0.0)
        while user_balance < needed_amount:
            try:
                add_money = float(input("How much would you like to add to your balance? \n>> "))
                if add_money <= 0:
                  print("Please enter valid money...")
                  continue

                user_balance += add_money
                user["balance"] = user_balance
                print(f"Your updated balance: {user_balance:.2f} AZN")
                 
            except ValueError:
                  print("Invalid amount, please try again...")
        

    def customer_menu(self, email=None):
        while True:

            for index, item in enumerate(CUSTOMER_MENU, start=1):
                print(f"[{index}] \033[32m {item} \033[0m")
            print("[0] \033[31m Exit\033[0m")
            print("[-1] \033[31m Go back\033[0m")

            try:
                menu_choise = int(input("\033[36mEnter your choice: \n>> \033[0m"))
                
            except (ValueError, IndexError):
                print("Invalid choice, Try again....")
                continue

            if menu_choise == 1:
                self.account.show_balance(email)
            elif menu_choise == 2:
                self.account.add_balance_account(email)
            elif menu_choise == 3:
                self.account.change_password(email)
            elif menu_choise == 4:
                self.account.history()
            elif menu_choise == -1:
                return
            elif menu_choise == 0:
                print("\033[33mThank you for visiting Codeffe! Goodbye...\033[0m")
                time.sleep(1)
                sys.exit()    
            else:
                print("\033[31mInvalid choice, try again...\033[0m")
                return True
            

