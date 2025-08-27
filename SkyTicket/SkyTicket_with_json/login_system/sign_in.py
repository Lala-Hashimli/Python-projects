from accounts.customer import Customer
from security_checker import EmailValidatior, PasswordValidator, PhoneValidator, PassportValidator, BirthdayValidator


class Signin:
    def __init__(self, customer: Customer,
                check_email:EmailValidatior, 
                check_password:PasswordValidator,
                check_phone:PhoneValidator,
                check_passport:PassportValidator,
                check_birthday: BirthdayValidator):
            
            self.customer = customer
            self.check_email = check_email
            self.check_password = check_password
            self.check_phone = check_phone
            self.check_passport = check_passport
            self.check_birthday = check_birthday

    def signin(self):
        fullname = input("\033[36mEnter your fullname: \n>> \033[0m").title()

        # check email
        while True:
            email = input("\033[36mEnter your email: \n>> \033[0m")
            self.check_email.email = email
            if self.check_email.check_email():
                break
        # check password
        while True:
            password = input("\033[36mEnter your password: \n>> \033[0m")
            self.check_password.password = password
            if self.check_password.check_password():
                break
        # check mobile phone
        while True:
            mobile_phone = input("Enter mobile phone (+994XXXXXXXXX): \n>> ")
            self.check_phone.phone = mobile_phone
            if self.check_phone.check_phone():
                break
        # check passport
        while True:
            passport = input("Enter passport(Format: AZ1234567): \n>> ")
            self.check_passport.passport = passport
            if self.check_passport.check_passport():
                break
        
        # check birthday
        while True:
            birthday = input("Enter your birth date (YYYY-MM-DD): \n>> ")
            if self.check_birthday.validate_birth_date(birthday):
                break
        
        self.customer.signin(fullname, email, password, mobile_phone, passport, birthday)