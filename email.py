from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import dotenv_values
from pydantic import BaseModel, EmailStr
from typing import List 
from .models import User
import jwt


config_credentials = dotenv_values(".env")

conf = ConnectionConfig(
    MAIL_USERNAME = config_credentials['EMAIL'],
    MAIL_PASSWORD = config_credentials['PASS'],
    MAIL_FROM = config_credentials['EMAIL'],
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_TLC = True,
    MAIL_SSL = False,
    USE_CREDENTIALS = True
) 

class EmailSchema(BaseModel):
    email: List[EmailStr]
    
async def send_email(email: EmailSchema, instance: User):
    token_data = {
        "id" : instance.id,
        "user_name" : instance.username,
    }
    token = jwt.encode(token_data, config_credentials["SECRETS"], algorithm='HS256')
    
    template = f"""
        <!DOCTYPE html>
        <html>
            <head>
                
            </head> 
            <body>
                <div style="display: flex; flex-direction: column; justify-content: center; align-items: center;">
                     <h3>Account Verification</h3><br>
                     <p>Thanks for shopping at Jumia! Please click on the button below to verify your account.</p>
                     
                     <button style="background: purple; border: none; outline: none; padding: 1rem; width: 160px; ">
                        <a href"https://localhost:8000/verification/?token={token}" style="color: white; text-decoratiom: none;">Verify Your Email</a>
                     </button
                     
                     <p>
                        Kindly ignore this message if you didn't register with Jumia.      Thank you
                     </p>
                </div>
            </body>
        </html
    """
    
    message = MessageSchema(
        subject="Jumia Account Verification",
        recipients=email, #LIST OF RECIPIENTS
        body=template,
        subtype="html"
    )
    
    fm = FastMail(conf)
    await fm.send_message(message=message)