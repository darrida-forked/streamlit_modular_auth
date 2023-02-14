from dataclasses import dataclass
import streamlit as st
from streamlit_cookies_manager import CookieManager
from streamlit_modular_auth.protocols import UserAuth, UserStorage, ForgotPasswordMessage, AuthCookies
from streamlit_modular_auth._handlers import (
    DefaultAuthCookies,
    DefaultForgotPasswordMsg,
    DefaultUserAuth,
    DefaultUserStorage,
)

# from login import Login
# from models import DefaultPageModel
# from views import DefaultPageView
from streamlit_modular_auth._cookie_manager import _initialize_cookie_manbager


cookies = _initialize_cookie_manbager()


@dataclass
class ModularAuth:
    """
    Arguments:
    -----------
    1. self
    2. auth_token : The unique authorization token received from - https://www.courier.com/email-api/
    3. company_name : This is the name of the person/ organization which will send the password reset email.
    4. width : Width of the animation on the login page.
    5. height : Height of the animation on the login page.
    6. logout_button_name : The logout button name.
    7. hide_menu_bool : Pass True if the streamlit menu should be hidden.
    8. hide_footer_bool : Pass True if the 'made with streamlit' footer should be hidden.
    9. lottie_url : The lottie animation you would like to use on the login page (https://lottiefiles.com/featured)
    10. hide_registration : Pass True if 'Create Account' option should be hidden from Navigation.
    11. hide_forgot_password : Pass True if 'Forgot Password?' option should be hidden from Navigation.
    11. hide_account_management : Pass True if all options other than 'Login' should be hidden from Navigation.
    12. custom_authentication : Option to pass custom authentication class that inherits from
        StreamlitDefaultUserAuth (see information further below).
    13. custom_user_storage : Option to pass custom user storage class that inherits from
        StreamLitDefaultUserStorage (see information further below).
    """

    cookies: CookieManager = cookies
    state = st.session_state
    login_expire: int = 7200
    login_width: int = 200
    login_height: int = 250
    login_lottie_url: str = ""
    login_hide_menu: bool = False
    login_hide_footer: bool = False
    login_hide_registration: bool = False
    login_hide_forgot_password: bool = False
    login_hide_account_management: bool = False
    login_label: str = "Login"
    logout_button_name: str = "Logout"
    plugin_user_auth: UserAuth = DefaultUserAuth()
    plugin_user_storage: UserStorage = DefaultUserStorage()
    plugin_forgot_password_msg: ForgotPasswordMessage = DefaultForgotPasswordMsg()
    plugin_auth_cookies: AuthCookies = DefaultAuthCookies()
    confg = {}
