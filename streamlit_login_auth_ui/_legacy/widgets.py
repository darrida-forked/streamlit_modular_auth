from streamlit_login_auth_ui._widgets import Login, cookies
from streamlit_login_auth_ui._handlers import DefaultAuthCookies


class __login__(Login):
    """Builds the UI for the Login/Sign Up page and manages all authentication logic."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_username(self, cookies=cookies):
        return DefaultAuthCookies().get_username(cookies)
