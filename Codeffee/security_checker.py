import re

class PasswordValidator:
    def __init__(self, password):
        self.password = password

    def check_password(self):
        if len(self.password) < 8:
            print("\033[31mThe password must be at least 8 characters long\033[0m")
            return False
        
        if not re.search(r"[A-Z]", self.password):
            print("\033[31mThe password must contain at least 1 uppercase letter\033[0m")
            return False
        
        if not re.search(r"[a-z]", self.password):
            print("\033[31mThe password must contain at least 1 lowercase letter\033[0m")
            return False
            
        if not re.search(r"[0-9]", self.password):
            print("\033[31mPassword must contain at least 1 digit\033[0m")
            return False
        

        print("\033[32mPassword accepted\033[0m")
        return True


class EmailValidatior:
    def __init__(self, email):
        self.email = email


    def check_email(self):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, self.email):
            print("\033[31mEmail is not in the correct format\033[0m")
            return False


        print("\033[32mEmail is correct\033[0m")    
        return True