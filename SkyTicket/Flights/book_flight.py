import sys
import json
from accounts.customer import Customer
from Flights.flight_manager import FlightManager


class BookFlight:
    def __init__(self, customer: Customer=None, flight_manager: FlightManager=None):
        self.customer = customer
        self.flight_manager = flight_manager


    def book_flight(self, flights, flight_manager=None):

        from Flights.seat_map import SeatMap
        from Flights.ticket_pdf import Ticket

        if flight_manager:
            self.flight_manager = flight_manager
        

        self.seat_map = SeatMap()


        asking = input("\033[36mDo you want to book a flight? (yes/no): \n>> \033[0m").strip().lower()
        if asking == "yes":
            try:
                choice = int(input("\033[36mEnter the flight number you want to book: \n>> \033[0m"))
                if choice < 1 or choice > len(flights):
                    print("\033[31mInvalid flight number. Please try again...\033[0m")
                    return
            except ValueError:
                print("\033[31mInvalid input. Please enter a number...\033[0m")
                return
                
            selected_flight = flights[choice - 1]
            self.seat_map.display_seat_map(selected_flight)

            while True:
                selected_seat = input("\033[36mEnter the seat you want to book (1A): \n>> \033[0m").strip().upper()

                found = False
                for class_name in selected_flight["seats"]:
                    if selected_seat in selected_flight["seats"][class_name]:
                        if selected_flight["seats"][class_name][selected_seat] == "booked":
                            print("\033[31m Seat already booked. Please choose another seat...\033[0m")
                            found = True
                            break

                        selected_class = class_name
                        found = True
                        break

                if not found:
                    print("\033[31mInvalid seat selection. Please try again...\033[0m")
                    return

                self.seat_map.display_seat_map(selected_flight, selected_seat)
                
                confrim = input("\033[36mDo you confirm your booking? (yes/no): \n>> \033[0m").strip().lower()
                if confrim == "yes":
                    break
                elif confrim == "no":
                    print("\033[33mSelection canceled. Choose another seat...\033[0m")
                    continue

            # check balance
            users = self.customer.load_users()
            email = input("\033[36mEnter your email: \n>> \033[0m").strip()
            for num in range(len(users)):
                if users[num]["email"] == email:
                    user = users[num]
                    while user["balance"] < selected_flight["price"][selected_class]:
                        print("\033[31mInsufficient balance. Please top up your account...\033[0m")
                        increasing_balance = input("Do you want to increase your balance? (yes/no): \n>> \033[0m").strip().lower()
                        if increasing_balance == "yes":
                            from accounts.account import Account
                            self.account = Account(self.customer)
                            self.account.add_balance_account(email)

                            users = self.customer.load_users()
                            for num in range(len(users)):
                                if users[num]["email"] == email:
                                    user = users[num]
                                    print(f"\033[31mYour current balance is: {user['balance']}\033[0m")
                                    break
                        else:
                            print("\033[31mBooking canceled for insufficient balance...\033[0m")
                            return
                    
            # payment
            user["balance"] -= selected_flight["price"][selected_class]

            selected_flight["seats"][selected_class][selected_seat] = "booked"

            user["bookings"].append({
                "flight_id": selected_flight["flight_id"],
                "airline": selected_flight["airline"],
                "from": selected_flight["from_city"],
                "to": selected_flight["to_city"],
                "seat": selected_seat,
                "price": selected_flight["price"][selected_class],
                "date": selected_flight["date"],
                "time": selected_flight["departure_time"]
            })
            # save changes
            self.customer.save_users(users)

            print("\033[92mFlight booked successfully!\033[0m")
            self.ticket = Ticket(user, selected_flight, selected_seat, selected_class)
            self.ticket.generate_ticket_pdf()
            with open("private_data/booked_flights.json", "w") as file:
                json.dump([], file)
            
            sys.exit()


