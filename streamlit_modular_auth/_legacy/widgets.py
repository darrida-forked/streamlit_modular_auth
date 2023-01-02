from streamlit_modular_auth._widgets import Login, cookies
from streamlit_modular_auth._handlers import DefaultAuthCookies, CourierForgotPasswordMsg


class __login__(Login):
    """Builds the UI for the Login/Sign Up page and manages all authentication logic."""

    def __init__(self, auth_token, company_name, **kwargs):
        super().__init__(**kwargs)
        self.password_reset = CourierForgotPasswordMsg(auth_token, company_name)

    def get_username(self, cookies=cookies):
        return DefaultAuthCookies().get_username(cookies)
