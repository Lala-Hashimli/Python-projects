import re
import datetime

class PasswordValidator:
    def __init__(self, password=None):
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
    def __init__(self, email=None):
        self.email = email


    def check_email(self):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, self.email):
            print("\033[31mEmail is not in the correct format\033[0m")
            return False


        print("\033[32mEmail is correct\033[0m")    
        return True
    

class PhoneValidator:
    def __init__(self, phone=None):
        self.phone = phone

    def check_phone(self):
        pattern = r"^\+994\d{9}$"
        if not re.match(pattern, self.phone):
            print("Invalid phone number. Format: +994XXXXXXXXX")
            return False
        
        print("Phone number accepted!")
        return True
    
class PassportValidator:
    def __init__(self, passport=None):
        self.passport = passport

    
    def check_passport(self):
        pattern = r"^AZ\d{7}$"
        if not re.match(pattern, self.passport):
            print("Invalid passport number. Format: AZ1234567")
            return False
        
        print("Passport number accepted!")
        return True


class BirthdayValidator:
    def __init__(self):
        pass

    def validate_birth_date(self, birth_date_str):
        
        birth_date = datetime.datetime.strptime(birth_date_str, "%Y-%m-%d").date()
        today = datetime.date.today()
        age = (today - birth_date).days // 365

        if birth_date > today:
            print("Birth date cannot be in the future")
            return False
        elif age < 12:
            print("You must be at least 12 years old to register")
            return False
        else:
            print("Birth date is valid")
            return True
        