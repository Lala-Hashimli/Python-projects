from food_stock import *
from drink_stoke import *
from payment import *
from receipt import *
from customer import *
from prettytable import PrettyTable
from datetime import datetime
from time import sleep
from os import system


# menu
def menu():
   while True:
      print("\n=== MENU ===")
      for index, category in enumerate(food_stock.keys(), start=1):
         print(f"\n[{index}] {category}")
      print("\n[0] Exit") 

      try:
         menu_index = int(input("\nChoose menu what you want: \n>> "))
         if menu_index == 0:
            system("clear")
            print("\nExited.Thank you :)")
            exit()
   

         menu_choice = list(food_stock.keys())[menu_index-1]
         system("clear")
         print(f"\n{menu_choice}:")

         for index, item in enumerate(food_stock[menu_choice], start=1):
               item_amount = food_stock[menu_choice][item]["amount"]
               print(f"\n[{index}] {item}: {item_amount} AZN")

         print("\n[0] Go back")
         print("\n[-1] Exit")
         result = choosing_item_from_catagory(menu_choice)
         if result:
            food_drink_choice, quantity = result
            return menu_choice, food_drink_choice, quantity



      except (IndexError, ValueError):
         print("\nInvalid choice. Try again...")
         continue   
             
def choosing_item_from_catagory(menu_choice):
   while True:
      item_index = int(input("\nChoose food/drink what you want (or 0 to go back, -1 to exit): \n>> "))
      if item_index == -1:
         system("clear")
         print("Exited.Thank you :)")
         exit()
      elif item_index == 0:
         system("clear")
         break
      else:
         try:
            food_drink_choice = list(food_stock[menu_choice].keys())[item_index-1]
            quantity = int(input(f"How many '{food_drink_choice}' would you like to order? \n>> "))
            return food_drink_choice, quantity
         except IndexError:
            print("\nInvalid choice. Try again...")
            continue


# open and close working 
time_now = datetime.now().hour
if 9 <= time_now or time_now < 1:
   print("\nWelcome to KFC. You can place an order")
else:
   print("\nKFC is currently closed. Please check back after 09:00")
   exit()


def show_product_table(basket:list): 
      combined_basket = {}
      basket_table = PrettyTable(["Quantity", "Product", "Amount", "Total"])

      for product in basket:
         product_name = product["Name"]
         if product_name not in combined_basket:
            combined_basket[product_name] = {
               "Name": product_name,
               "Amount":  product["Amount"],
               "Quantity": product["Quantity"],
               "Total": product["Total"]
            }
         else:
            combined_basket[product_name]["Quantity"] += product["Quantity"]
            combined_basket[product_name]["Total"] += product["Total"]

      # print basket table
      for item in combined_basket.values():
         
         basket_table.add_row([
            item["Quantity"], 
            item["Name"], 
            f"{item["Amount"]:.2f}",
            f"{item["Total"]:.2f}"
         ])

         
      basket_total = sum(item["Total"] for item in combined_basket.values())
      
      total_table = PrettyTable()
      total_table.add_row(["Basket total:", f"{basket_total:.2f}"])
      total_table.header = False

      print(total_table) 
      print(basket_table)
      return combined_basket, basket_total

# checking user accounts
while True:
   user_name = input("enter your name: \n>> ").title()
   if user_name in customers:
      if customers[user_name]["balance"] <= 0:
         print("There is not enough balance in your account.")
      elif customers[user_name]["limit"] <= 0:
         print("You haven't made enough attempt.")
      else:
         f"\nWelcome back, {user_name}"
   else:
      print(f"\nUser {user_name} not found. Creating a new account...")
      for i in range(3, 0, -1):
         print(f"Please wait {i} seconds...")
         sleep(1)
      try:
         customers[user_name] = {
            "balance": randint(20,70),
            "limit" : 2
         }
         print(f"\n Created account for {user_name}")
      except ValueError:
            print("Invalid input for balance or limit. Try again.\n")
            continue

   user_amount, user_limit = customers[user_name]["balance"], customers[user_name]["limit"]
   print(f"You have {user_amount} azn in your account")
   break


menu_choice, food_drink_choice, quantity = menu()
total_amount = 0
basket = []
while True:
   item_price = food_stock[menu_choice][food_drink_choice]["amount"]
   # basket
   basket.append({
      "Name": food_drink_choice,
      "Amount":  item_price,
      "Quantity": quantity,
      "Total": item_price * quantity
   })

   # combine same products
   combined_basket, basket_total = show_product_table(basket)
   
   # remove
   asking_remove = input("Do you want to remove food/drink to your basket? (yes/no): \n>>").lower()
   if asking_remove == "yes":
      if not basket:
         print("Your basket is empty")
         continue
      else:
         print("Your basket:")
         for index, item in enumerate(combined_basket.values(), start=1):
            print(f"[{index}] {item["Quantity"]} x {item["Name"]} : {item["Total"]:.2f}")
         try:
            remove_index = int(input("Enter number of the product that you want to remove ('0' to cancel): \n>>"))
            if remove_index == 0:
               pass
            else:
               selected_item = list(combined_basket.values())[remove_index-1]
               remove_product = selected_item["Name"]
               basket = [item for item in basket if item["Name"] != remove_product]
               print(f"{remove_product} removed from your basket")
               combined_basket, basket_total = show_product_table(basket)

         except (IndexError, ValueError):
            print("Invalid input, Try again")   
   while True:
      # asking for add  
      user_asking = input("\nDo you want to add food/drink to your basket? (yes/no): \n>> ").lower()
      if user_asking == "yes":
         while True:
            selected_catagory = input("\nWhich category would you like to choose? (same/another): \n>> ").lower()
            if selected_catagory == "same":
               food_drink_choice, quantity = choosing_item_from_catagory(menu_choice)
               break
            elif selected_catagory == "another":
               system("clear")
               menu_choice,food_drink_choice, quantity = menu()
               break
            else:
               print("Invalid input. Please enter 'same' or 'another'")
         break

      elif user_asking.lower() == "no":
         print("Lets pay!")
         while user_amount < basket_total:
            print(f"You do not have enough money in your account. You need more {basket_total-user_amount:.2f} AZN")
            try:
               add_money = float(input("How much would you like to add to your balance? \n>> "))
               if add_money <= 0:
                  print("Please enter valid money...")
                  continue
               customers[user_name]["balance"]+= add_money
               user_amount = customers[user_name]["balance"]
               print(f"Your updated balance: {user_amount:.2f} AZN")
            except ValueError:
                  print("Invalid amount, please try again...")
      
         total_amount, user_amount, user_limit = payment(basket, total_amount, customers, user_name)
         print(f"Payment completed. You have {user_amount:.2f} AZN  left in your account")
         exit()
      else:
         print("Please, enter only yes or no")
         continue
   


