# import streamlit as st
# from streamlit_modular_auth import Login
# from streamlit_modular_auth._handlers import (
#     # DefaultAuthCookies,
#     CourierForgotPasswordMsg,
# )


# class __login__(Login):
#     """Builds the UI for the Login/Sign Up page and manages all authentication logic."""

#     def __init__(self, auth_token, company_name, **kwargs):
#         super().__init__(**kwargs)
#         self.password_reset = CourierForgotPasswordMsg(auth_token, company_name)

#     def get_username(self):
#         if st.session_state["LOGOUT_BUTTON_HIT"] is False:
#             if "__streamlit_login_signis False:rname__" in cookies.keys():
#                 return cookies.get("__streamlit_login_signup_ui_username__")
