import os 
import time
from config import FILTER

class FlightMenu:
    def __init__(self, customer=None):
        self.customer = customer
        self.flights = None
        self.book_flight = None 

    def flight_menu(self):
        from Flights.flight_manager import FlightManager
        from Flights.book_flight import BookFlight

        self.flights = FlightManager()
        self.book_flight = BookFlight(customer=self.customer)

        print("\n\033[1;34mAll Available Flights:\033[0m")
        self.flights.show_flights()
                    
        self.results = self.flights.search_flights()

        if not self.results:
            print("\033[31mNo flights found\033[0m")
     
        while True:
            asking = input("\033[36mDo you want to use a filter? (yes/no): \n>> \033[0m").strip().lower()
            if asking == "yes":
                from Flights.flight_filter import FlightFilter
                self.filter = FlightFilter()
                print("\n\033[1;34mAvailable Filters:\033[0m")

                for index, item in enumerate(FILTER, start=1):
                    print(f"[{index}] \033[32m Priced by {item} \033[0m")
                print("[0] \033[31m Exit\033[0m")
                try:
                    filter_choice = int(input("\033[36mEnter your choice: \n>> \033[0m"))
                    if filter_choice == 1:
                        self.filter.filter_by_price(self.results)
                        break
                    elif filter_choice == 2:
                        self.filter.filter_by_duration(self.results)
                        break
                    elif filter_choice == 3:
                        self.filter.filter_by_airline(self.results)
                        break
                    elif filter_choice == 4:
                        self.filter.filter_by_time(self.results)
                        break
                    elif filter_choice == 0:
                        continue
                    else:
                        print("\033[31Invalid choice, try again...\033[0m")
                        continue
                except (ValueError, IndexError):
                    print("\nInvalid choice. Try again...")
                    continue

            elif asking == "no":
                print("\033[33mNo filter applied\033[0m")
                break

            else:
                print("\033[31mInvalid input. Please enter 'yes' or 'no'\033[0m")
                continue

        self.book_flight.book_flight( flights=self.results, flight_manager=self.flights)