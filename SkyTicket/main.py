import time
import os
import sys
from security_checker import EmailValidatior, PasswordValidator, PhoneValidator, PassportValidator, BirthdayValidator
from accounts.customer import Customer
from accounts.account import Account
from config import AUTH_MENU, MAIN_MENU



class AviabiletReservationSystem:
    def __init__(self, customer: Customer):
        self.customer = customer
        

    def run(self):
        from login_system.log_in import Login
        from login_system.sign_in import Signin
        print("Welcome to \033[36mSky\033[32mTicket\033[0m")

        
        while True:
            time.sleep(1.5)
            os.system("clear")
            for index, item in enumerate(AUTH_MENU, start=1):
                print(f"[{index}] \033[32m {item} \033[0m")
            print("[0] \033[31m Exit\033[0m")

            try:
                user_choise = int(input("\033[36mEnter your choice: \n>> \033[0m"))

                if user_choise == 0:
                    print("\033[33mThank you for visiting SkyTicket! Goodbye...\033[0m")
                    time.sleep(1)
                    sys.exit()

                elif user_choise == 1:
                    # log in
                    log_in = Login(self.customer, self)
                    log_in.login()

                elif user_choise == 2:
                    # sign in
                    sign_in = Signin(self.customer,
                                    EmailValidatior(),
                                    PasswordValidator(),
                                    PhoneValidator(),
                                    PassportValidator(),
                                    BirthdayValidator())
                    sign_in.signin()
                
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
                if user["isAdmin"] == False:
                    self.customer.customer_menu(email)
                    
                return
        print("User not found")



    def main_menu(self):
        from Flights.flights_menu import FlightMenu
        while True:
            time.sleep(1.5)
            os.system("clear")
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
                    # Flights
                    menu = FlightMenu(self.customer)
                    menu.flight_menu()

                elif user_choise == 0:
                    # exit
                    print("\033[33mThank you for visiting SkyTicket! Goodbye...\033[0m")
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
customer.account = account



app = AviabiletReservationSystem(customer)

try:
    app.run()
except SystemExit:
    print("Program exited.")
except KeyboardInterrupt:
    print("\nProgram interrupted. Exiting...")