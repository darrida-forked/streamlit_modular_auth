import streamlit as st


class DefaultForgotPasswordMsg:
    def send(self, username: str, email: str, reset_password: str) -> None:
        st.write("Talk to your system administrator.")
