import streamlit as st
from streamlit_login_auth_ui.utils import ForgotPassword


class ForgotPasswordTest(ForgotPassword):
    def __init__(self, message: str):
        self.method_name = "Very Insecure"
        self.message = message

    def send_password(
        auth_token: str, username: str, email: str, company_name: str, password: str, 
        message: str
    ) -> None:
        st.write(f"{message}: {password}")