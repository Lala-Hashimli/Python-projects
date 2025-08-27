from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

class Ticket:

    def __init__(self, user, flight, seat, class_name=None):
        self.user = user
        self.flight = flight
        self.seat = seat
        self.class_name = class_name 

    def generate_ticket_pdf(self):
        
        filename = f"ticket_{self.user["fullname"].replace(" ", "_")}_{self.flight["flight_id"]}_{self.seat}.pdf"
        file_path = os.path.join("bookings", filename)

        
        os.makedirs("bookings", exist_ok=True)

        
        pdf = canvas.Canvas(file_path, pagesize=A4)
        width, height = A4

        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawCentredString(width / 2, height - 50, "SkyTicket Airline Ticket")

        pdf.setFont("Helvetica", 12)
        pdf.drawString(100, height - 100, f"Name: {self.user["fullname"]}")
        pdf.drawString(100, height - 120, f"Email: {self.user["email"]}")
        pdf.drawString(100, height - 140, f"From: {self.flight["from_city"]}")
        pdf.drawString(100, height - 160, f"To: {self.flight["to_city"]}")
        pdf.drawString(100, height - 180, f"Date: {self.flight["date"]}")
        pdf.drawString(100, height - 200, f"Time: {self.flight["departure_time"]}")
        pdf.drawString(100, height - 220, f"Seat: {self.seat}")
        pdf.drawString(100, height - 240, f"Airline: {self.flight["airline"]}")
        pdf.drawString(100, height - 260, f"Price: {self.flight["price"][self.class_name]} AZN")

        pdf.setFont("Helvetica-Oblique", 10)
        pdf.drawCentredString(width / 2, 50, "Thank you for booking with SkyTicket!")

        pdf.save()
        print(f"\033[1;32mTicket saved as '{file_path}'\033[0m")


