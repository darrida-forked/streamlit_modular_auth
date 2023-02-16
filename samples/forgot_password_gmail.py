import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from streamlit_modular_auth.protocols import ForgotPasswordMessage


class ForgotPasswordGmail(ForgotPasswordMessage):
    def __init__(self, email_user: str):
        self.method_name = "Gmail"
        self.email_user = email_user

    def __build_message_body(self, username, password):
        text = f"""\
            Hi! {username},

            Your temporary login password is: {password}

            Login and change the password as soon as possible.
        """

        html = f"""\
            <html>
            <body>
                <p>
                    Hi! {username},<br>
                    <br>
                    Your temporary login password is: {password}<br>
                    <br>
                    Login and change the password as soon as possible.
                </p>
            </body>
            </html>
        """
        return text, html

    def send(
        self,
        auth_token: str,
        username: str,
        email: str,
        company_name: str,
        password: str,
    ) -> None:
        from_email = self.email_user
        receiver_email = email

        message = MIMEMultipart("alternative")
        message["Subject"] = f"{company_name}: Login Password!"
        message["From"] = from_email
        message["To"] = receiver_email

        # Set plain/html MIMEText objects
        text, html = self.__build_message_body(username, password)
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        message.attach(part1)
        message.attach(part2)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(from_email, auth_token)
            server.sendmail(self.email_user, receiver_email, message.as_string())
