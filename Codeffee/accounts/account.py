import json
import pandas as pd

class Account:
    def __init__(self, customer , filename="basket_db.json"):
        from accounts.customers import Customer
        self.customer = customer
        self.filename = filename


    def load_basket(self):
        with open(self.filename, 'r') as file:
            return json.load(file)
        

    def show_balance(self, email=None):
        users = self.customer.load_users()

        for user in users:
            if user["email"] == email:
                print(f"You have {user["balance"]} AZN")
                return
        else:
            print("Email not found")
            

    def add_balance_account(self, email=None):
        users = self.customer.load_users()
        
        amount = float(input("\033[33mEnter amount to add:\n>> \033[0m"))
        
        for user in users:
            if user["email"] == email:
                user["balance"] += amount
                print(f"{amount} AZN added to {email}'s account.")
                break
        else:
            print("User not found.")

        self.customer.save_users(users)

    def change_password(self, email=None):
        from security_checker import PasswordValidator
        users = self.customer.load_users()
        
        for user in users:
            if user["email"] == email:
                while True:
                    new_password = input("Enter new password:\n>> ")
                    if PasswordValidator(new_password):
                        user["password"] = new_password
                        print(f"Password for {email} has been updated.")
                        break
            else:
                print("Email not found.")

        self.customer.save_users(users)


    def history(self):
        basket_data = self.load_basket()
        fullname = input("\033[36mEnter customer's full name:\n>> \033[0m").title()

        all_rows = []
        baskets = basket_data.get("basket", {})
        for date, users in baskets.items():
            if fullname in users:
                for item in users[fullname]:
                    row = {
                        "Date": date,
                        "Time": item["Time"],
                        "Product Name": item["Name"],
                        "Amount": item["Amount"],
                        "Quantity": item["Quantity"],
                        "Total": item["Total"]
                    }
                    all_rows.append(row)

        if all_rows:
            df = pd.DataFrame(all_rows)
            print(f"\nPurchase history for {fullname}:\n")
            print(df.to_string(index=False))
            
            filename = f"{fullname.replace(" ", "_")}_purchase_history.xlsx"
            df.to_excel(filename, index=False)
            print(f"{filename} Excel file saved seccefully")
        else:
            print("No history found for this user.")
    
    