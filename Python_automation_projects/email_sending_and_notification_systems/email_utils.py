import os
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from settings import *


def create_email(sender_email, recipient_email, EMAIL_SUBJECT, body, html=False):
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = EMAIL_SUBJECT
    
    if html:
        msg.attach(MIMEText(body, "html"))
    else:
        msg.attach(MIMEText(body, "plain"))
    return msg

def attach_file(msg, file_path):
    try:
        with open(file_path, "rb") as f:
            mime_base = MIMEBase("application", "octet-stream")
            mime_base.set_payload(f.read())

        encoders.encode_base64(mime_base)
        mime_base.add_header(
            "Content-Disposition",
            f"attachment; filename={file_path.split('/')[-1]}"
        )
        msg.attach(mime_base)
        return True
    except Exception as e:
        print(f"⚠️ Could not attach file: {e}")
        return False
    
def attach_inline_image(msg, image_path, cid):
    
    try:
        with open(image_path, "rb") as f:
            img = MIMEImage(f.read())
            img.add_header("Content-ID", f"<{cid}>")
            img.add_header("Content-Disposition", "inline", filename=os.path.basename(image_path))
            msg.attach(img)
    except Exception as e:
        print(f"⚠️ Could not attach inline image {image_path}: {e}")