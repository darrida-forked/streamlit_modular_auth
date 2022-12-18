import streamlit as st
from streamlit_login_auth_ui.protocols import ForgotPasswordMessage


class ForgotPasswordCustomMsgTest:
    def __init__(self, message: str):
        self.method_name = "Very Insecure"
        self.message = message

    def send_password(self, auth_token: str, username: str, email: str, company_name: str, password: str) -> None:
        st.write(f"{self.message}: {password}")