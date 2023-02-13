from dataclasses import dataclass
import streamlit as st
from streamlit_modular_auth.protocols import UserAuth, UserStorage, ForgotPasswordMessage, AuthCookies
from streamlit_modular_auth._handlers import (
    DefaultAuthCookies,
    DefaultForgotPasswordMsg,
    DefaultUserAuth,
    DefaultUserStorage,
)
from streamlit_modular_auth._cookie_manager import _initialize_cookie_manbager


cookies = _initialize_cookie_manbager()


@dataclass
class Config:
    auth: UserAuth = DefaultUserAuth()
    user_storage: UserStorage = DefaultUserStorage()
    forgot_password_msg: ForgotPasswordMessage = DefaultForgotPasswordMsg()
    auth_cookies: AuthCookies = DefaultAuthCookies()
    cookies = cookies
    state = st.session_state


config = Config()
