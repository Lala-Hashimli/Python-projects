from receipt import *



def payment(basket, total_amount, customers, user_name):
   for item in basket:
      total_amount += item["Total"]
   
   customers[user_name]["balance"] -= total_amount
   customers[user_name]["limit"] -= 1
   generate_receipt(user_name, total_amount, basket)
      
   
   return total_amount, customers[user_name]["balance"], customers[user_name]["limit"]
   
