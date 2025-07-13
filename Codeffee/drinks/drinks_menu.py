import time
import sys
import json
import os
from basket.basket import Basket
from accounts.customers import Customer
from receipt.receipt import Receipt
from datetime import datetime




class DrinkMenu:
    def __init__(self, basket:Basket, customer: Customer, user_name, receipt: Receipt):
        self.basket = basket
        self.customer = customer
        self.user_name = user_name
        self.receipt = receipt
        self.payment_done = False


    def load_drink_stock(self, filename="drinks/drink_stock.json"):
        with open(filename, "r") as file:
            return json.load(file)
 
    # drink stock  category
    def drink_category_menu(self):
        

        while True:
            try:
                os.system("clear")
                drink_category = list(self.load_drink_stock().keys())
                for index, category in enumerate(drink_category, start=1):
                    print(f"\n[{index}] {category}")
                print("\n[0] Exit") 
                print("\n[-1] Go back") 

                try:
                    category_index = int(input("\033[36mChoose category what you want (or 0 to go back, -1 to exit): \n>> \033[0m"))
                    
                    if category_index == 0:
                        print("\033[33mThank you for visiting Codeffe! Goodbye...\033[0m")
                        time.sleep(1)
                        sys.exit()
                    
                    elif category_index == -1:
                        return
                    
                    elif 1 <= category_index <= len(drink_category):
                        selected_category = drink_category[category_index - 1]
                        self.drink_item_menu(selected_category)

                        if self.payment_done:
                            return   
                    else:
                        print("\nInvalid choice. Try again...")
               
                except (IndexError, ValueError):
                    print("\nInvalid choice. Try again...")
                    continue
                        
            except (IndexError, ValueError):
                print("\nInvalid choice. Try again...")
                continue



    # drink stock  category 
    def drink_item_menu(self, selected_category):
        while True:

            print(f"\033[93m{selected_category}\033[0m")
            drinks = self.load_drink_stock()[selected_category]
            drinks_names = list(drinks.keys())
            
            for index, item in enumerate(drinks_names, start=1):
                item_amount = drinks[item]["amount"]
                print(f"\n[{index}] {item}: \033[96m{item_amount} ₼ \033[0m")
            print("\n[0] Exit") 
            print("\n[-1] Go back")
            
            try:
                drink_index = int(input("\033[36mChoose drink what you want (or 0 to go back, -1 to exit): \n>> \033[0m"))
                
                if drink_index == 0:
                    print("\033[33mThank you for visiting Codeffe! Goodbye...\033[0m")
                    time.sleep(1)
                    sys.exit()
                
                elif drink_index == -1:
                    break
                
                elif 1 <= drink_index <= len(drinks_names):
                    drink_name = drinks_names[drink_index-1]
                    drink_price = drinks[drink_name]["amount"]
                    quantity = int(input(f"How many '{drink_name}' would you like to order? \n>> "))

                    current_time = datetime.today().strftime("%H:%M:%S")
                    self.basket.add_item_to_basket(drink_name, drink_price, quantity, current_time)
                    
                    self.basket.save_basket()

                    basket_total = self.remove_item()
                        
                    self.add_item_again(basket_total)
                    
                    if self.payment_done:
                        return
 
                else:
                    print("\nInvalid choice. Try again...")    

            except (IndexError, ValueError):
                print("\nInvalid choice. Try again...")   

    def remove_item(self):
        asking_remove = input("Do you want to remove food/drink to your basket? (yes/no): \n>>").lower()
                    
        os.system("clear")
        if asking_remove == "yes":
            combined_basket, basket_total = self.basket.show_product_table()
            self.basket.remove_item(combined_basket)
            
            self.basket.show_product_table()
            return basket_total
        else:
            _ , basket_total = self.basket.show_product_table()
            return basket_total


    # payment
  
    def payment(self, user, total):
        users = self.customer.load_users()
        for i, u in enumerate(users):
            if u["email"] == user["email"]:
                if u["balance"] >= total:
                    users[i]["balance"] -= total
                    self.customer.save_users(users)
                    self.receipt.generate_receipt(u, total, self.basket.current_basket)
                    print("\033[32mPayment completed. Receipt generated. Exiting...\033[0m") 
                    return True
                else:
                    print(f"\033[31mPayment failed.\033[0m")
                    return False
        return False


    # add again
    def add_item_again(self, basket_total):
        while True:
            asking_add_again = input("\nDo you want to add food/drink to your basket? (yes/no): \n>> ").lower() 
            
            if asking_add_again == "yes":
                return
            
            elif asking_add_again == "no":
                print("Lets pay")
                users = self.customer.load_users()
                
                for user in users:
                    if user["fullname"] == self.user_name:
                        
                        
                        # add balance
                    
                        if user["balance"] < basket_total:
                            needed_amount = basket_total - user["balance"]
                            print(f"You do not have enough money in your account. You need more {needed_amount:.2f} AZN")
                            self.customer.add_balance(user, needed_amount)
                            users = self.customer.load_users()  
                            for updated_user in users:
                                if updated_user["fullname"] == self.user_name:
                                    user = updated_user
                                    break
                        
                        # payment
                        success = self.payment(user, basket_total)
                        if success:
                            self.payment_done = True
                            print("\033[32mExiting...\033[0m")
                            time.sleep(1.5)
                            return
                        else:
                            
                            print("\033[31mPayment failed. Exiting...\033[0m")
                            time.sleep(2)
                            sys.exit()  
                        break
               
                        print(f"\033[93mYour current balance: {user['balance']:.2f} AZN\033[0m")
                

                return
                                 
                        
            else:
                print("Please, enter only enter 'yes' or 'no'")
                
