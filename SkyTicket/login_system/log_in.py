from accounts.customer import Customer


class Login:

    def __init__(self, customer: Customer, main_system):
        self.customer = customer
        self.main_system = main_system
    
    def login(self):
        while True:

            email = input("\033[36mEnter your email: \n>> \033[0m")
            password = input("\033[36mEnter your password: \n>> \033[0m")

            if self.customer.login(email, password):
                self.main_system.main_menu()
            else:
                print("\033[31mLogin failed\033[0m")



