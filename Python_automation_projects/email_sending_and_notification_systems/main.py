import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from settings import sender_email, app_password, file_to_attach, image_path
from email_utils import create_email, attach_file, attach_inline_image


excel_file = "table.xlsx"  
cid = "image"
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()  
server.login(sender_email, app_password)
msg = MIMEMultipart()
msg["Subject"] = "Notification"


df = pd.read_excel(excel_file)

for index, row in df.iterrows():
    recipient_email = row["Email"]
    recipient_name = row.get("Name", "")
    EMAIL_SUBJECT = row.get("Message", "Hello!")   

    body = f"Hello {recipient_name},\n\n{EMAIL_SUBJECT}\n\nBest regards"

    create_email(sender_email, recipient_email, EMAIL_SUBJECT, body)
    attach_file(msg, file_to_attach)
    attach_inline_image(msg, image_path, cid)

    try:
        server.sendmail(sender_email, recipient_email, msg.as_string())
        print(f"✅ Sent: {recipient_email}")
    except Exception as e:
        print(f"❌ Failed: {recipient_email}, Reason: {e}")


server.quit()
