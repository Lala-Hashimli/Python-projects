import pandas as pd


from reportlab.lib.pagesizes import mm
from reportlab.pdfgen import canvas
from datetime import datetime
from random import randint
from prettytable import PrettyTable
from PIL import Image
from reportlab.lib.utils import ImageReader
from datetime import datetime

class Receipt:
    
    def process_image(self, image):
        img = Image.open(image).convert("RGBA")
        background = Image.new("RGBA", img.size, (255, 255, 255, 255))
        background.paste(img, mask=img.split()[3])
        
        converted_image = "converted_icon.jpg"
        background.convert("RGB").save(converted_image, format="JPEG")
        return ImageReader(converted_image)
        
    def generate_receipt(self, customer_name, total_amount, basket):
        if isinstance(customer_name, dict):
            fullname = customer_name["fullname"]
        else:
            fullname = str(customer_name)
        queue_number = randint(1000,9999)
        now = datetime.now().strftime("%d-%m-%Y %H-%M-%S")

        filename = f"{fullname} {now}.pdf"
        icon = "Codeffee.png"
        self.process_image(icon)
        icon_image = "converted_icon.jpg"
        width = 125 * mm
        height = 150 * mm

        pdf = canvas.Canvas(filename, pagesize=(width, height))

        y = height - 30



        pdf.setFont("Courier-Bold", 14)
        pdf.drawCentredString(width / 2 , y, "Welcome to Codeffee")
        y -= 20

        # icon
        pdf.drawInlineImage(icon_image, width / 2 - 45, y - 65, width=80, height=80)
        y -= 60

        # order
        order_num_table = PrettyTable(["Order#"])

        order_num_table.add_row([queue_number])
        pdf.setFont("Courier", 10)
        for line in str(order_num_table).splitlines():
            pdf.drawString(width / 2 - 30, y-10, line)
            y -= 12
        y -= 32

        hyphen = " -" * 17
        pdf.drawString(10, y+12, hyphen)

        # customer name and date-time
        pdf.setFont("Courier", 9)
        pdf.drawString(15, y, f"Customer: {fullname}")
        y -= 16
        pdf.drawString(15, y, f"Date: {now}")
        y -= 13
        hyphen = " -" * 19
        pdf.drawString(10, y, hyphen)
        

        
        y -= 16
        
        # products
        combined_basket = {}
        
        
        for item in basket:
            product_name = item["Name"]
            if product_name not in combined_basket:
                combined_basket[product_name] = {
                    "Name": product_name,
                    "Amount":  item["Amount"],
                    "Quantity": item["Quantity"],
                    "Total": item["Total"]
                }
            else:
                combined_basket[product_name]["Quantity"] += item["Quantity"]
                combined_basket[product_name]["Total"] += item["Total"]

        df = pd.DataFrame.from_dict(combined_basket, orient='index')
        df = df[["Quantity", "Name", "Amount", "Total"]]
        df.columns = ["Count", "Product", "Amount", "Total"]

        pdf.setFont("Courier", 10)
        
        for i, line in df.to_string(index=False).splitlines():
            pdf.drawString(15, y, line)
            if i == 0:
                 y -= 22
            else:
                y -= 18

        # total
        pdf.setFont("Courier", 10)
        pdf.drawString(13, y, f"Total: {total_amount}")
        y -= 18

        pdf.setFont("Courier", 12)
        pdf.drawCentredString(width / 2, y-8, "Visit Codeffee-az.com")
        pdf.setFont("Courier-Bold", 14)
        pdf.drawCentredString(width / 2, y-20, "Thank you for choosing Codeffee!")
        
        
        pdf.save()