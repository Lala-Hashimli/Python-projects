from reportlab.lib.pagesizes import mm
from reportlab.pdfgen import canvas
from datetime import datetime
from random import randint
from prettytable import PrettyTable
from PIL import Image
from reportlab.lib.utils import ImageReader
from datetime import datetime



def process_image(image):
    img = Image.open(image).convert("RGBA")
    background = Image.new("RGBA", img.size, (255, 255, 255, 255))
    background.paste(img, mask=img.split()[3])
    
    converted_image = "converted_icon.jpg"
    background.convert("RGB").save(converted_image, format="JPEG")
    return ImageReader(converted_image)


def generate_receipt(customer_name, total_amount, basket):
    queue_number = randint(1000,9999)
    now = datetime.now().strftime("%d-%m-%Y %H-%M-%S")

    filename = f"receipt {now}.pdf"
    icon = "kfc_icon.jpg"
    process_image(icon)
    icon_image = "converted_icon.jpg"
    width = 125 * mm
    height = 150 * mm

    pdf = canvas.Canvas(filename, pagesize=(width, height))

    y = height - 30



    pdf.setFont("Courier-Bold", 14)
    pdf.drawCentredString(width / 2 , y, "Welcome to KFC")
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
    y -= 30

    hyphen = " -" * 17
    pdf.drawString(10, y+12, hyphen)

    # customer name and date-time
    pdf.setFont("Courier", 9)
    pdf.drawString(15, y, f"Customer: {customer_name}")
    y -= 15
    pdf.drawString(15, y, f"Date: {now}")
    y -= 12
    hyphen = " -" * 19
    pdf.drawString(10, y, hyphen)
    

    
    y -= 15
    
    # products
    combined_basket = {}
    receipt_total = PrettyTable(["Count", "Product", "Amount", "Total"])
    
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
    
    for item in combined_basket.values():
        quantity, product, amount, total = item["Quantity"], item["Name"], item["Amount"], item["Total"]
        receipt_total.add_row([quantity, product, f"{amount:.2f}", f"{total:.2f}"])

    pdf.setFont("Courier", 10)
    for line in str(receipt_total).splitlines():
        pdf.drawString(13, y, line)
        y -= 14

    # total
    total_table = PrettyTable()
    total_table.add_row(["Total:", f"{total_amount:.2f}"])
    total_table.header = False
    pdf.setFont("Courier", 10)
    for line in str(total_table).splitlines():
        pdf.drawString(13, y, line)
        y -= 10

    pdf.setFont("Courier", 12)
    pdf.drawCentredString(width / 2, y-8, "Visit kfc-az.com")
    pdf.setFont("Courier-Bold", 14)
    pdf.drawCentredString(width / 2, y-20, "Thank you for choosing KFC!")
    
    
    pdf.save()

