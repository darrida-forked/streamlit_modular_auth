import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from streamlit_login_auth_ui.utils import ForgotPassword


class ForgotPasswordGmail(ForgotPassword):
    def __init__(self, email_user: str, email_password: str):
        self.method_name = "Gmail"
        self.email_user = email_user
        self.email_password = email_password

    def send_password(
        auth_token: str, username: str, email: str, company_name: str, password: str, 
        email_user: str,
    ) -> None:
        from_email = email_user
        receiver_email = email

        message = MIMEMultipart("alternative")
        message["Subject"] = f"{company_name}: Login Password!"
        message["From"] = from_email
        message["To"] = receiver_email

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

        # Set plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        message.attach(part1)
        message.attach(part2)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(from_email, auth_token)
            server.sendmail(email_user, receiver_email, message.as_string())