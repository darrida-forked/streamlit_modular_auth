from dataclasses import dataclass, field

import streamlit as st
from streamlit_cookies_manager import CookieManager

from streamlit_modular_auth._cookie_manager import _initialize_cookie_manbager
from streamlit_modular_auth.handlers.auth_cookies import DefaultAuthCookies
from streamlit_modular_auth.handlers.storage.json_storage import DefaultJSONUserAuth, DefaultJSONUserStorage
from streamlit_modular_auth.handlers.forgot_password_msg import DefaultForgotPasswordMsg
from streamlit_modular_auth.protocols import AuthCookies, ForgotPasswordMessage, UserAuth, UserStorage

cookies = _initialize_cookie_manbager()


@dataclass
class ModularAuth:
    """[Name]
    [Description]
    - Lottie animations can be found here: https://lottiefiles.com/featured

    Args:
        width (int): Define login page animation widget
        height (int): Define login page animation height
        logout_button_name (str): Define login button name
        hide_menu (bool): Remove upper-right menu button
        hide_footer (bool): Remove "Made with Streamlit" footer
        lottie_url (str, Optional): URL for lottie animation on login page
        hide_registration (bool): Remove "Create Account" option from menu
        hide_forgot_password (bool): Remove "Forgot Password" option from menu
        hide_account_management (bool): Remove all options other than 'Login' from menu
        plugin_user_auth (UserAuth): Protocol to add custom authentication functionality
        plugin_user_storage (UserStorage): Protocol to add custom user storage functionality
        plugin_forgot_password_msg (ForgotPasswordMessage): Protocol to add custom forgot password messaging
        plugin_auth_cookies (AuthCookies): Protocol to add custom authentication cookies functionality
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
    plugin_user_auth: UserAuth = DefaultJSONUserAuth()
    plugin_user_storage: UserStorage = DefaultJSONUserStorage()
    plugin_forgot_password_msg: ForgotPasswordMessage = DefaultForgotPasswordMsg()
    plugin_auth_cookies: AuthCookies = DefaultAuthCookies()
    config: dict = field(default_factory=lambda: {})

    def set_sqlite_storage(self):
        from streamlit_modular_auth.handlers.storage.sqlmodel_storage import DefaultDBUserAuth, DefaultDBUserStorage

        self.plugin_user_auth = DefaultDBUserAuth()
        self.plugin_user_storage = DefaultDBUserStorage()
        self.config["set_sqlite_storage"] = True

    def enable_admin_page(self):
        from streamlit_modular_auth._apps.admin.page import admin_page

        self.admin_page = admin_page
        self.config["enable_default_admin_page"] = True
