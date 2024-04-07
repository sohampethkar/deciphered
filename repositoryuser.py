import smtplib
from email.message import EmailMessage
import asyncio

class SendEmailVerify:
    @staticmethod
    async def send_verify(token, max_attempts=3):
        email_address = "cairocoders0711@gmail.com"
        email_password = "cairocoders-ednalan"

        # create email
        msg = EmailMessage()
        msg['Subject'] = "Email subject"
        msg['From'] = email_address
        msg['To'] = "clydeymojica0130@gmail.com"
        msg.set_content(
            f"""\
            verify account        
            http://localhost:8080/user/verify/{token}
            """,
        )

        for attempt in range(1, max_attempts + 1):
            try:
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(email_address, email_password)
                    await asyncio.sleep(0)  # Yield control to the event loop
                    smtp.send_message(msg)
                print("Email sent successfully!")
                return  # Exit the function if email sent successfully
            except Exception as e:
                print(f"Error sending email (attempt {attempt}/{max_attempts}): {e}")
        
        print("Max attempts reached. Unable to send email.")
