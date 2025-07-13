import json
import os
import time

class FlightManager:
    def __init__(self, filename="private_data/flights.json"):
        self.filename = filename


        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as file:
                return json.dump([], file)

    def load_flights(self):
        with open(self.filename, "r") as file:
            return json.load(file)
        
    def save_flights(self, flights):
        with open(self.filename, "w") as file:
            return json.dump(flights, file, indent=4)
        
    def show_flights(self):
        flights = self.load_flights()
        if not flights:
            print("No flights avaible")
            return
        for index, flight in enumerate(flights, start=1):
            print(f"[{index}] {flight["from_city"]} → {flight["to_city"]} | {flight["date"]} | {flight["departure_time"]} | {flight["airline"]} | {flight["price"]} AZN")
    
    def search_flights(self):
        from Flights.flight_filter import FlightFilter
        flights = self.load_flights()
        filtered_flights = FlightFilter()

        print("\nPlease enter flight search details:\n")
        while True:
            from_city = input("\033[36mFrom City: \n>> \033[0m ").title()
            to_city = input("\033[36mTo City: \n>> \033[0m").title()
            date = input("\033[36mDate (YYYY-MM-DD): \n>> \033[0m")
            
            if not from_city or not to_city or not date:
                print("\033[31mAll fields are required\033[0m")
                continue

            import datetime
            try:
                datetime.datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                print("\033[31m Invalid date format. Use YYYY-MM-DD.\033[0m")
                return
            
            results = []
            for flight in flights:
                if flight["from_city"].lower() == from_city.lower() and flight["to_city"].lower() == to_city.lower() and flight["date"] == date:
                    results.append(flight)
                    
            filtered_flights.save_filtered_flights(results)

            if results:
                print("\n\033[1;34mFound Flights:\033[0m")
                for index, flight in enumerate(results, start=1):
                    print(f"[{index}] {flight["from_city"]} → {flight["to_city"]} | {flight["date"]} | {flight["departure_time"]} | {flight["airline"]} | {flight["price"]} AZN")
                return results
            else:
                print("No matching flights")
                continue   
        
            
            