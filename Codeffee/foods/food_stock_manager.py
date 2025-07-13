import json

class FoodStockManager:
    def __init__(self, filename="foods/food_stock.json"):
        with open(filename, "r") as file:
            self.stock = json.load(file)


    def add_category(self):
        while True:
            category = input("\033[36mEnter category:\n>> \033[0m").title().strip()

            if category in self.stock:
                print(f"\033[31m{category} already exists. Try another...\033[0m")
            else:
                self.stock[category] = {}
                print(f"\033[32m{category} has been added\033[0m")
                break

    def add_new_product(self):
        category = input("\033[36mEnter category:\n>> \033[0m").title().strip()
        product_name = input("\033[35mEnter food name add to category:\n>> \033[0m").title().strip()

        while True:
            try:
                amount = float(input("\033[36mEnter price of food: \n>> \033[0m"))
                break
            except ValueError:
                print("\033[31m Invalid amount... \033[0m")
        
        if category not in self.stock:
            self.stock[category]={}
        
        self.stock[category][product_name] = {"amount": amount}
        print(f"\033[32m{product_name} added to {category} with {amount} ₼\033[0m")


    def remove_category(self):
        category = input("\033[36mEnter category to remove:\n>> \033[0m").title().strip()

        if category in self.stock:
            check_certainty = input("\033[31mAre you sure you want to delete the entire category? (yes/no)\n>> \033[0m").lower().strip()

            if check_certainty == "yes":
                del self.stock[category]
                print(f"\033[33m{category} category has been remeoved   \033[0m")
            else:
                print("\033[36m Canceled \033[0m")
        else:
            print("\033[31m Category not found \033[0m")

    def remove_product(self):
        category = input("\033[36mEnter category:\n>> \033[0m").title().strip()
        product_name = input("\033[35mEnter food name to remove:\n>> \033[0m").title().strip()  

        if (category in self.stock 
            and product_name in self.stock[category]):

            del self.stock[category][product_name]
            print(f"\033[33m{product_name} removed from {category}\033[0m")

        else:
            print("\033[31m Category or product not found \033[0m")

    def update_price(self):
        category = input("\033[36mEnter category:\n>> \033[0m").title().strip()
        product_name = input("\033[35mEnter food name: \n>> \033[0m").title().strip()

        while True:
            try:
                new_price = float(input("\033[36mEnter price of food: \n>> \033[0m"))
                break
            except ValueError:
                print("\033[31m Invalid price... \033[0m")
        
        if (category in self.stock
            and product_name in self.stock[category]):
            
            self.stock[category][product_name]["amount"] = new_price
            print(f"\033[32m {product_name} of {category} updated to {new_price}\033[0m")


    def save_to_file(self, filename="foods/food_stock.json"):
        with open(filename, "w") as file:
            json.dump(self.stock, file, indent=4)
        print("\033[32m Stock saved successfully \033[0m")


        