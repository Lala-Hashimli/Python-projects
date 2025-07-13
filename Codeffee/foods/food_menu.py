import time
import sys
import json
import os
import datetime
from basket.basket import Basket
from drinks.drinks_menu import DrinkMenu


class FoodMenu:
    def __init__(self, basket:Basket, drinksMenu: DrinkMenu):
        self.basket = basket
        self.drinkMenu = drinksMenu

    def load_food_stock(self, filename="foods/food_stock.json"):
        with open(filename, "r") as file:
            return json.load(file)
        

    # food stock category 
    def food_category_menu(self):
        

        while True:
            try:
                os.system("clear")
                food_category = list(self.load_food_stock().keys())

                for index, category in enumerate(food_category, start=1):
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
                    
                    elif 1 <= category_index <= len(food_category):

                        selected_category = food_category[category_index - 1]
                        self.food_item_menu(selected_category)
                             
                    else:
                        print("\nInvalid choice. Try again...")


                except (IndexError, ValueError):
                    print("\nInvalid choice. Try again...")
                    continue
                        
            except (IndexError, ValueError):
                print("\nInvalid choice. Try again...")
                continue

    # food stock items
    def food_item_menu(self, selected_category):
        while True:
            print(f"\033[93m{selected_category}\033[0m")

            foods = self.load_food_stock()[selected_category]
            foods_names = list(foods.keys())

            for index, item in enumerate(foods_names, start=1):
                item_amount = foods[item]["amount"]
                print(f"\n[{index}] {item}: \033[96m{item_amount} ₼ \033[0m")
            print("\n[0] Exit") 
            print("\n[-1] Go back")
            
            try:
                food_index = int(input("\033[36mChoose drink what you want (or 0 to go back, -1 to exit): \n>> \033[0m"))
                if food_index == 0:
                    print("\033[33mThank you for visiting Codeffe! Goodbye...\033[0m")
                    time.sleep(1)
                    sys.exit()

                elif food_index == -1:
                    break
                elif 1 <= food_index <= len(foods_names):
                    food_name = foods_names[food_index-1]
                    drink_price = foods[food_name]["amount"]

                    quantity = int(input(f"How many '{food_name}' would you like to order? \n>> "))

                    current_time = datetime.today().strftime("%H:%M:%S")
                    self.basket.add_item_to_basket(food_name, drink_price, quantity, current_time)
                    
                    self.basket.save_basket()

                    # remove item
                    basket_total = self.drinkMenu.remove_item()

                    # add item again
                    self.drinkMenu.add_item_again(basket_total)

                    return
                else:
                    print("\nInvalid choice. Try again...") 

            except (IndexError, ValueError):
                print("\nInvalid choice. Try again...")