import json
import os
from prettytable import PrettyTable
from datetime import datetime


class Basket:
    def __init__(self, filename="private_data/basket_db.json", user_name=None):
        self.filename = filename
        self.user_name = user_name
        self.basket = self.load_basket()
        self.current_basket = []
    
    def load_basket(self):

        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
               data = json.load(file)
               basket_data = data.get("basket", {})
               current_date = datetime.today().strftime("%d-%m-%Y")
               return basket_data.get(current_date, {}).get(self.user_name, [])
        
        return []

    def remove_duplicates(self, basket_list):
        """
        Every time a new item is added to the basket, the previous items are also duplicated.
        For example, initially the basket was: basket = [1], and when I added 2 to the basket,
        the JSON looked like this: basket = [1, 1, 2].
        If I then added 3, it would look like this:
        basket = [1, 1, 2, 1, 2, 3]
        This prevents duplication in the basket.
        """
        seen = set()
        unique_list = []

        for item in basket_list:
            identifier = tuple(sorted(item.items()))
            if identifier not in seen:
                seen.add(identifier)
                unique_list.append(item)
        return unique_list

    def save_basket(self):
        
        today = datetime.today().strftime("%d-%m-%Y") 
        data = {}
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
               data = json.load(file)

        
        if "basket" not in data:
            data["basket"] = {}

        if today not in data["basket"]:
            data["basket"][today] = {}

        if self.user_name not in data["basket"][today]:
            data["basket"][today][self.user_name] = []



        combined = data["basket"][today][self.user_name] + self.current_basket
        data["basket"][today][self.user_name] = self.remove_duplicates(combined)

        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=4)
        
        

    # add
    def add_item_to_basket(self, item_name, item_amount, quantity, current_time):
                
        item_total = item_amount * quantity
        self.current_basket.append({
        "Name": item_name,
        "Amount":  item_amount,
        "Quantity": quantity,
        "Total": item_total,
        "Time": current_time
        })
        

        self.show_product_table()
    
    
    # remove
    def remove_item(self, combined_basket):

        print("Your basket:")
        for index, item in enumerate(combined_basket.values(), start=1):
            print(f"[{index}] {item["Quantity"]} x {item["Name"]} : {item["Total"]:.2f}")
        
        try:
            remove_index = int(input("Enter number of the product that you want to remove ('0' to cancel): \n>>"))
            if remove_index == 0:
               return
            else:
               
               selected_item = list(combined_basket.values())[remove_index-1]
               remove_product = selected_item["Name"]
               self.basket = [item for item in self.basket if item["Name"] != remove_product]
               print(f"{remove_product} removed from your basket")
               self.save_basket()
               self.show_product_table()

        except (IndexError, ValueError):
            print("Invalid input, Try again")

        


    def show_product_table(self):
        combined_basket = {}
        basket_table = PrettyTable(["Quantity", "Product", "Amount", "Total"])

        for product in self.current_basket:
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

        # print basket 
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
    



            

