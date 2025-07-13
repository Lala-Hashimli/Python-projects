

class SeatMap:
    def __init__(self):
        pass

    def display_seat_map(self, flight, selected_seat=None):
        print("\n\033[1;34mPlane Seat Map\033[0m\n")

        # Business class
        print("     \033[1;33mBUSINESS CLASS\033[0m")
        print("    -------------------")
        print("Row  A   B     C   D")

        for row in [1, 2]:
            print(f" {row}   ", end="")
            for col in ["A", "B", "C", "D"]:
                seat = f"{row}{col}"
                status = flight["seats"]["business"].get(seat, "available")
                symbol = "[ ]"

                if seat == selected_seat:
                    symbol = "[\033[1;32m✓\033[0m]"
                elif status == "booked":
                    symbol = "[\033[1;31mX\033[0m]"
                print(symbol, end=" ")
                if col == 'B':
                    print("  ", end="")
            print()

            

        # Comfort class
        print("\n     \033[1;35mCOMFORT CLASS\033[0m")
        print("    -------------------")
        print("Row   A   B     C   D")

        for row in [3, 4]:
            print(f" {row}   ", end="")
            for col in ["A", "B", "C", "D"]:
                seat = f"{row}{col}"
                status = flight["seats"]["comfort"].get(seat, "available")
                symbol = "[ ]"
                if seat == selected_seat:
                    symbol = "[\033[1;32m✓\033[0m]"
                elif status == "booked":
                    symbol = "[\033[1;31mX\033[0m]"
                print(symbol, end=" ")
                if col == 'B':
                    print("  ", end="")
            print()



        # Economy class
        print("\n     \033[1;36mECONOMY CLASS\033[0m")
        print("    -------------------------")
        print("Row   A   B   C   D   E   F")

        for row in range(5, 7):
            print(f" {row}   ", end="")
            for col in ["A", "B", "C", "D", "E", "F"]:
                seat = f"{row}{col}"
                status = flight["seats"]["economy"].get(seat, "available")
                symbol = "[ ]"
                if seat == selected_seat:
                    symbol = "[\033[1;32m✓\033[0m]"
                elif status == "booked":
                    symbol = "[\033[1;31mX\033[0m]"
                print(symbol, end=" ")
            print()

        print("[ ] - Available")
        print("[\033[1;31mX\033[0m] - Booked")
        print("[\033[1;32m✓\033[0m] - Selected\n")