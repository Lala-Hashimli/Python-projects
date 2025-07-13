import json
import sys
import time
from config import *
from accounts.customers import *
from accounts.account import *
from drinks.drink_stock_manager import DrinkStockManager
from foods.food_stock_manager import FoodStockManager
class Admin:
    def __init__(self, customer:Customer, account: Account, drink_manager:DrinkStockManager, food_manager: FoodStockManager, filename="users.json"):
        self.costumer = customer
        self.filename = filename
        self.account = account
        self.drink_manager = drink_manager
        self.food_manager = food_manager


    def load_users(self):
        with open(self.filename, 'r') as file:
            return json.load(file)
        
    
    def admin_menu(self,email=None):
        from basket.basket_stat import BasketStats

        while True:
            for index, item in enumerate(ADMIN_MENU, start=1):
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
            elif menu_choise == 5:
                stats = BasketStats("basket_db.json")
                stats.start_dowland_excel()
                asking_stats = input("\033[36mDo you want to see statistics? (yes/no): \n>> \033[0m").lower()
                if asking_stats.strip() == "yes":
                    stats.plot_statistics()
                else:
                    print("\033[33mStatistics not shown.\033[0m")
            elif menu_choise == 6:
                asking_menu = int(input("Which menu do you want to add category:(drink(0) / food(1)) \n>> "))
                if asking_menu == 0:
                    self.drink_manager.add_category()
                elif asking_menu == 1:
                    self.food_manager.add_category()
            elif menu_choise == 7:
                asking_menu = int(input("Which menu do you want to add product to category:(drink(0) / food(1)) \n>> "))
                if asking_menu == 0:
                    self.drink_manager.add_new_product()
                elif asking_menu == 1:
                    self.food_manager.add_new_product()
            elif menu_choise == 8:
                asking_menu = int(input("Which menu do you want to update price of product:(drink(0) / food(1)) \n>> "))
                if asking_menu == 0:
                    self.drink_manager.update_price()
                elif asking_menu == 1:
                    self.food_manager.update_price()
            elif menu_choise == 9:
                asking_menu = int(input("Which menu do you want to remove category:(drink(0) / food(1)) \n>> "))
                if asking_menu == 0:
                    self.drink_manager.remove_category()
                elif asking_menu == 1:
                    self.food_manager.remove_category()
            
            elif menu_choise == 10:
                asking_menu = int(input("Which menu do you want to remove product of category:(drink(0) / food(1)) \n>> "))
                if asking_menu == 0:
                    self.drink_manager.remove_product()
                elif asking_menu == 1:
                    self.food_manager.remove_product()
            elif menu_choise == 11:
                asking_menu = int(input("Which menu do you want to save file:(drink(0) / food(1)) \n>> "))
                if asking_menu == 0:
                    self.drink_manager.save_to_file()
                elif asking_menu == 1:
                    self.food_manager.save_to_file()
            elif menu_choise == -1:
                return
               
            elif menu_choise == 0:
                print("\033[33mThank you for visiting Codeffe! Goodbye...\033[0m")
                time.sleep(1)
                sys.exit()  




