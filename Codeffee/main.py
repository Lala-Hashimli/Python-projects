import os
import time
import sys
from datetime import datetime
from drinks.drinks_menu import DrinkMenu
from foods.food_menu import FoodMenu
from drinks.drink_stock_manager import DrinkStockManager
from foods.food_stock_manager import FoodStockManager
from receipt.receipt import Receipt
from config import *
from accounts.customers import *
from accounts.admin import *
from basket.basket import *
from security_checker import *

# open and close time 
time_now = datetime.now().hour
if 9 <= time_now or time_now < 1:
   print("\nWelcome to \033[34mCode\033[33mffe\033[0m. You can place an order")
else:
   print("\Codeffee is currently closed. Please check back after 09:00")
   exit()




class Menu:
    def __init__(self, customer:Customer, 
                admin:Admin,
                drinks_menu: DrinkMenu,
                foods_menu: FoodMenu,
                check_email:EmailValidatior, 
                check_password:PasswordValidator):
        
        self.customer = customer
        self.admin = admin
        self.current_user = None
        self.basket = Basket()
        self.drinks_menu = drinks_menu
        self.foods_menu = foods_menu
        self.check_email = check_email
        self.check_password = check_password

        
    # MENU
    def run(self):
        print("Welcome to \033[34mCode\033[33mffe\033[0m")
        
        while True:
            time.sleep(1.5)
            os.system("clear")
            for index, item in enumerate(AUTH_MENU, start=1):
                print(f"[{index}] \033[32m {item} \033[0m")
            print("[0] \033[31m Exit\033[0m")

            try:
                user_choise = int(input("\033[36mEnter your choice: \n>> \033[0m"))

                if user_choise == 1:
                    while True:

                        # log in
                        email = input("\033[36mEnter your email: \n>> \033[0m")
                        password = input("\033[36mEnter your password: \n>> \033[0m")
                        if self.customer.login(email, password):
                            """
                            emailden istifade ederek fullname cixarilir ve  current_user -a teyin edilir
                            basketde hansi user ne aldigini yaddasda saxlamasi, nezaret ucun 
                            hemde user oz hesabinin history-dan ne zaman ne aldigina baxa biler
                            """
                            self.current_user = self.customer.get_fullname(email)
                            self.basket = Basket(user_name=self.current_user)

                            self.drinks_menu.basket = self.basket
                            self.drinks_menu.user_name = self.current_user

                            self.foods_menu.basket = self.basket
                            self.foods_menu.drinkMenu = self.drinks_menu
                            
                            if not self.drinks_menu.payment_done:
                                self.main_menu() 
                            break
                        else:
                            print("\033[31mLogin failed\033[0m")

                elif user_choise == 2:
                    # sign in
                    fullname = input("\033[36mEnter your fullname: \n>> \033[0m").title()
                    # check email
                    while True:
                        email = input("\033[36mEnter your email: \n>> \033[0m")
                        self.check_email.email = email

                        if self.check_email.check_email():
                            break

                    # check password
                    while True:
                        password = input("\033[36mEnter your password: \n>> \033[0m")
                        self.check_password.password = password
                        if self.check_password.check_password():
                            break

                    self.customer.signin(fullname, email, password)
                elif user_choise == 0:
                    print("\033[33mThank you for visiting Codeffe! Goodbye...\033[0m")
                    time.sleep(1)
                    sys.exit()
                else:
                    print("\033[31Invalid choice, try again...\033[0m")
                    continue

            except (IndexError, ValueError):
                print("\nInvalid choice. Try again...")
                continue


    def view_account(self, email):
        
        users = self.customer.load_users()
        for user in users:
            if user["email"] == email:
                if user["isAdmin"] == True:
                    self.admin.admin_menu(email)
                else:
                    self.customer.customer_menu(email)
                return
        print("User not found")




             

    def show_menu(self):
        while True:

            for index, item in enumerate(CATAGORY, start=1):
                print(f"[{index}] \033[32m {item} \033[0m")
            print("[0] \033[31m Exit\033[0m") 
            print("[-1] \033[31m Go back\033[0m") 

            try:
                menu_index = int(input("\033[36mEnter your choice: \n>> \033[0m"))
                
                print("\n\033[93m=== MENU ===\033[0m")
                if menu_index == 1:
                    print("\033[33mDrink:\033[0m")
                    for index, category in enumerate(self.drinks_menu.load_drink_stock().keys(), start=1):
                        print(f"\n[{index}] {category}")
                    print("\n[0]\033[31m Exit\033[0m") 
                    
                    self.drinks_menu.drink_category_menu()
                    
                    
                    
                elif menu_index == 2:
                    print("\033[33mFood:\033[0m")
                    
                    for index, category in enumerate(self.foods_menu.load_food_stock().keys(), start=1):
                        print(f"\n[{index}] {category}")
                    print("\n[0] Exit") 
                    print("\n[-1] Go back") 
                    
                    self.foods_menu.food_category_menu()

                    

                        
                elif menu_index == 0:
                    print("\033[33mThank you for visiting Codeffe! Goodbye...\033[0m")
                    time.sleep(1)
                    sys.exit()
                elif menu_index == -1:
                    return
                else:
                    print("\033[31Invalid choice, try again...\033[0m")
                    continue

            except (IndexError, ValueError):
                print("\nInvalid choice. Try again...")
                continue




    def main_menu(self):
        while True:
            for index, item in enumerate(MAIN_MENU, start=1):
                print(f"[{index}] \033[32m {item} \033[0m")
            print("[0] \033[31m Exit\033[0m") 

            try:

                user_choise = int(input("\033[36mEnter your choice: \n>> \033[0m"))

                if user_choise == 1:
                    # Account
                    email = input("\033[36mEnter your email: \n>> \033[0m")
                    self.view_account(email)
                    
                elif user_choise == 2:
                    # Menu
                    self.show_menu()
                elif user_choise == 0:
                    # exit
                    print("\033[33mThank you for visiting Codeffe! Goodbye...\033[0m")
                    time.sleep(1)
                    sys.exit()
                else:
                    print("\033[31Invalid choice, try again...\033[0m")   
                    continue

            except (IndexError, ValueError):
                print("\nInvalid choice. Try again...")
                continue


customer = Customer()
account = Account(customer)
drink_manager = DrinkStockManager()
food_manager = FoodStockManager()

customer.account = account

admin = Admin(customer, account, drink_manager, food_manager)

user_name = "guest"

basket = Basket(user_name=user_name)
receipt = Receipt()


drink_menu = DrinkMenu(basket, customer, user_name, receipt)
foods_menu = FoodMenu(basket, drink_menu)

check_email = EmailValidatior("")
check_password = PasswordValidator("")

app = Menu(customer, admin, drink_menu, foods_menu, check_email, check_password)


try:
    app.run()
except SystemExit:
    print("Program exited.")
except KeyboardInterrupt:
    print("\nProgram interrupted. Exiting...")
   


