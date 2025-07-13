import json
import pandas as pd
import matplotlib.pyplot as plt

class BasketStats:
    def __init__(self, filename="private_data/basket_db.json"):
        self.filename = filename
        self.data = None
        self.df = None

    def load_data(self):
        with open(self.filename, "r", encoding="utf-8") as file:
            self.data = json.load(file)
        print("\033[32m Basket data loaded successfully\033[0m")
        

    def to_dataframe(self):
        if not self.data:
            print("Data not loaded")
            return

        records = []
        for date, users in self.data["basket"].items():
            for user, items in users.items():
                for item in items:
                    records.append({
                        "Date": date,
                        "Time": item["Time"],
                        "Customer": user,
                        "Product": item["Name"],
                        "Amount": item["Amount"],
                        "Quantity": item["Quantity"],
                        "Total": item["Total"]
                    })

        self.df = pd.DataFrame(records)
        print("Data converted to DataFrame")

    def export_to_excel(self, output_file="purchase_history.xlsx"):
        self.df.to_excel(output_file, index=False)
        print(f"\033[32mExcel exported as '{output_file}' successfully")
        

    def plot_statistics(self):
        if self.df is not None:
            product_stats = self.df.groupby("Product")["Quantity"].sum().sort_values(ascending=False)
            plt.figure(figsize=(12, 6))
            product_stats.plot(kind="bar", color="skyblue")
            plt.title("Most Purchased Products")
            plt.ylabel("Total Quantity Sold")
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            plt.savefig("product_statistics.png")
            plt.show()
            print("Product statistics plotted and saved as 'product_statistics.png'.")
        else:
            print("DataFrame not available.")

    def start_dowland_excel(self):
        self.load_data()
        self.to_dataframe()
        self.export_to_excel()
        

