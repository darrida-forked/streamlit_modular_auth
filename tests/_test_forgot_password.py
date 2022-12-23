import streamlit as st


class ForgotPasswordCustomMsgTest:
    def __init__(self, message: str):
        self.method_name = "Very Insecure"
        self.message = message

    def send(self, username: str, email: str, password: str) -> None:
        st.write(f"{self.message}: {password}")
