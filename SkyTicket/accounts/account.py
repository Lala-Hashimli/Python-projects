import pandas as pd

from accounts.customer import Customer

class Account:
    def __init__(self, customer: Customer):
        self.customer = customer

    
    def show_balance(self, email=None):

        users = self.customer.load_users()

        for user in users:
            if user["email"] == email:
                print(f"You have {user["balance"]} AZN")
                return
        else:
            print("Email not found.")


    def add_balance_account(self, email=None):
        users = self.customer.load_users()
        
        try:
            amount = float(input("\033[33mEnter amount to add:\n>> \033[0m"))
            if amount <= 0:
                print("Amount must be greater than 0")
                return

            for user in users:
                if user["email"] == email:
                    user["balance"] += amount
                    print(f"{amount} AZN added to {email}'s account.")
                    break
            else:
                print("User not found.")

            self.customer.save_users(users)
            
        except ValueError:
            print("Invalid input. Please enter a valid number")

    def change_password(self, email=None):
        from security_checker import PasswordValidator
        users = self.customer.load_users()
        
        for user in users:
            if user["email"] == email:
                while True:
                    new_password = input("Enter new password:\n>> ")
                    if PasswordValidator(new_password):
                        user["password"] = new_password
                        print(f"Password for {email} has been updated")
                        break
            else:
                print("Email not found")

        self.customer.save_users(users)

    def bookings(self, email=None):
        users = self.customer.load_users()

        for user in users:
            if user["email"] == email:
                if user["bookings"]:
                    print("\033[1;34mYour Bookings:\033[0m")
                    all_bookings = []
                    for booking in user["bookings"]:
                        data = {
                            "Flight ID": booking["flight_id"],
                            "Airline": booking["airline"],
                            "From": booking["from"],
                            "To": booking["to"],
                            "Seat": booking["seat"],
                            "Price (AZN)": booking["price"],
                            "Date": booking["date"],
                            "Time": booking["time"],
                        }
                        all_bookings.append(data)
                    df = pd.DataFrame(all_bookings)
                    print(df.to_string(index=False))
                    df.to_excel(f"{user["fullname"].replace(' ', '_')}_bookings.xlsx", index=False)
                else:
                    print("\033[1;31mYou have no bookings yet\033[0m")

            

        