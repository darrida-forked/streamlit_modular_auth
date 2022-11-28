import os
import streamlit as st
from streamlit_login_auth_ui import __login__
from streamlit_login_auth_ui.utils import StreamlitUserAuth
from __test_user_storage import (
    # StreamLiteSQLAlchemyStorage, StreamLitSQLAlchemyAuth
    StreamlitTestAuth, StreamlitTestUserStorage
)


class CustomAuth(StreamlitUserAuth):
    def __init__(self, login_name=None, username=None, password=None):
        super().__init__(login_name, username, password)
    
    def check_usr_pass(self):
        if self.username == "custom_auth_user" and self.password == "custom_auth_pass":
            return True
        return False


hide_registration = True if os.environ.get("HIDE_REGISTRATION") == "true" else False
hide_account_management = True if os.environ.get("HIDE_ACCOUNT_MANAGEMENT") == "true" else False
hide_footer_bool = True if os.environ.get("HIDE_FOOTER") == "true" else False
hide_menu_bool = True if os.environ.get("HIDE_MENU") == "true" else False
logout_button_name = (
    os.environ.get("LOGOUT_BUTTON_NAME") if os.environ.get("LOGOUT_BUTTON_NAME") else "Logout"
)
if os.environ.get("CUSTOM_AUTH"):
    if os.environ.get("CUSTOM_AUTH") != "true":
        custom_authentication = CustomAuth(login_name=os.environ.get("CUSTOM_AUTH"))
    else:
        custom_authentication = CustomAuth()
else:
    custom_authentication = None

if os.environ.get("CUSTOM_USER_STORAGE") == "true":
        custom_authentication = StreamlitTestAuth(login_name="Test Login")
        custom_user_storage = StreamlitTestUserStorage()
else:
    custom_user_storage = None


__login__obj = __login__(
    auth_token = "courier_auth_token", 
    company_name = "Sample Name",
    width = 200, 
    height = 250, 
    logout_button_name = logout_button_name,
    hide_menu_bool = hide_menu_bool, 
    hide_footer_bool = hide_footer_bool, 
    lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json',
    hide_registration=hide_registration,
    hide_account_management=hide_account_management,
    custom_authentication=custom_authentication,
    custom_user_storage=custom_user_storage
)


LOGGED_IN = __login__obj.build_login_ui()


if LOGGED_IN == True:
    st.markdown("Your Streamlit Application Begins here!")