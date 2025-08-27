import sys
import json
import datetime
import os


class FlightFilter:
    def __init__(self, filename="private_data/filtered_data.json"):
        self.filename = filename

        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as file:
                return json.dump([], file)
    
    def save_filtered_flights(self,filtered_flights, filename=None):
        if not filename:
            filename = self.filename
        with open(filename, "w") as f:
            json.dump(filtered_flights, f, indent=4) 


    def display_flights(self, flights, seat_class=None):
        for index, flight in enumerate(flights, start=1):
            print(f"""[{index}] {flight["from_city"]} → {flight["to_city"]} | 
                {flight["date"]} | {flight["departure_time"]} | {flight["airline"]}\033[0m""")
            if seat_class:
                print(f"\033[32m{flight["price"][seat_class]} AZN ({seat_class.capitalize()})\033[0m")
            else:
                print(
                f"""\033[32m{flight['price']['economy']}₼ Economy\033[0m, 
                \033[33m{flight['price']['comfort']}₼ Comfort\033[0m, 
                \033[36m{flight['price']['business']}₼ Business\033[0m"""
                )
                    
    
    def filter_by_price(self, flights):

        print("\nWhich seat class do you want to filter by price?")
        print("[1] Business")
        print("[2] Comfort")
        print("[3] Economy")
        print("[0] Exit")
        print("[-1] Go back")

        class_map = {
            1: "business",
            2: "comfort",
            3: "economy"
        }


        while True:
            try:
                seat_choice = int(input("\033[36mSelect a seat class: \n>> \033[0m"))

                if seat_choice == 0:
                    sys.exit()
                    
                elif seat_choice == -1:
                    print("\033[33mGoing back...\033[0m")
                    return
                
                seat_class = class_map.get(seat_choice)
                if not seat_class:
                    print("\033[31mInvalid choice. Try again...\033[0m")
                    continue


                print("\n[1] Price → Low to high")
                print("[2] Price → High to low")

                
                def sort_by_price(flight, seat_class=seat_class):
                    return flight["price"][seat_class]
                
                choice = int(input("\033[36mSelect a filter: \n>> \033[0m"))
                
                reverse = True if choice ==  2 else False

                filtered = sorted(flights, key=sort_by_price, reverse=reverse)


                print("\n \033[1;34mSorted by price:\033[0m")
                self.display_flights(filtered, seat_class)
                self.save_filtered_flights(filtered)
                break
                
            except (ValueError, IndexError):
                print("\n\033[31mInvalid choice. Try again...\033[0m")
                continue

    
    
    def filter_by_duration(self, flights):
        def get_duration_minutes(flight):
            deperture_time = datetime.datetime.strptime(flight["departure_time"], "%H:%M")
            arrival_time = datetime.datetime.strptime(flight["arrival_time"], "%H:%M")

            duration = (arrival_time - deperture_time).total_seconds() / 60

            if duration < 0:
                duration += 24 * 60
            return duration
        

        try:
            max_duration = int(input("\033[36mEnter the maximum duration in minutes: \n>> \033[0m"))
        except ValueError:
            print("\033[31mInvalid input. Please enter a number.\033[0m")
            return
        
        filtered_flights = [flight for flight in flights if get_duration_minutes(flight) < max_duration]
        if not filtered_flights:
            print("\033[31mNo flights found under this duration\033[0m")
        else:
            print(f"Found {len(filtered_flights)} flights under {max_duration} minutes")
            
            self.display_flights(filtered_flights)
            self.save_filtered_flights(filtered_flights)
            
    
    def filter_by_airline(self, flights):
        airline_name = input("\033[36mEnter the airline name to filter: \n>> \033[0m").strip().title()
        filtered_airlines = [flight for flight in flights if flight["airline"].lower() == airline_name.lower()]
        if not filtered_airlines:
            print("\033[31mNo flights found for this airline\033[0m")
        else:
            print(f"{len(filtered_airlines)} flights found for {airline_name.title()}")
            self.display_flights(filtered_airlines)
            self.save_filtered_flights(filtered_airlines)

    def filter_by_time(self, flights):
        try:
            start_time = input("\033[36mStart time (HH:MM): \n>> \033[0m")
            end_time = input("\033[36mEnd time (HH:MM): \n>> \033[0m")

            start = datetime.datetime.strptime(start_time, "%H:%m").time()
            end = datetime.datetime.strptime(end_time, "%H:%m").time()
        except ValueError:
            print("\033[31mInvalid time format. Use HH:MM.\033[0m")
            return
        
        filtered_time = []
        for flight in flights:
            dep_time = datetime.datetime.strptime(flight["departure_time"], "%H:%m").time()

            if start <= end:
                #  12.00     15.00      19.00
                if start <= dep_time <= end:
                    filtered_time.append(dep_time)
                else:
                    # for 23.00 -> 04.50
                    #    02.00     22.00      02.00     05.30
                    if dep_time >= start or dep_time <= end:
                        filtered_time.append(dep_time)
                    
            if not filtered_time:
                print("\033[31mNo flights found\033[0m")
            else:
                print(f"\033[32m{len(filtered_time)} flights found between {start_time} and {end_time}\033[0m")
                self.display_flights(filtered_time)
                self.save_filtered_flights(filtered_time)
                

                


