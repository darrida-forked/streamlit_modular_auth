from streamlit_login_auth_ui._widgets import Login, cookies
from streamlit_login_auth_ui._handlers import DefaultAuthCookies, DefaultForgotPasswordMsg


class __login__(Login):
    """Builds the UI for the Login/Sign Up page and manages all authentication logic."""

    def __init__(self, auth_token, company_name, **kwargs):
        super().__init__(**kwargs)
        self.password_reset = DefaultForgotPasswordMsg(auth_token, company_name)

    def get_username(self, cookies=cookies):
        return DefaultAuthCookies().get_username(cookies)
