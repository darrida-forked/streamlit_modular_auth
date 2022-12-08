import os
from pathlib import Path
import streamlit as st
from streamlit_login_auth_ui import __login__
from streamlit_login_auth_ui.utils import UserAuth
from __test_user_storage import UserAuthTest, UserStorageTest
from __test_forgot_password import ForgotPasswordCustomMsgTest

import importlib

module_init = "streamlit_login_auth_ui"
file_path = Path(__file__).parent / "streamlit_login_auth_ui" / "__init__.py"
spec_init = importlib.util.spec_from_file_location(module_init, file_path)

module_utils = "streamlit_login_auth_ui.utils"
file_path = Path(__file__).parent / "streamlit_login_auth_ui" / "utils.py"
spec_utils = importlib.util.spec_from_file_location(module_utils, file_path)

module_widgets = "streamlit_login_auth_ui.widgets"
file_path = Path(__file__).parent / "streamlit_login_auth_ui" / "widgets.py"
spec_widgets = importlib.util.spec_from_file_location(module_widgets, file_path)

class CustomAuth(UserAuth):
    def __init__(self, login_name=None, username=None, password=None):
        super().__init__(login_name, username, password)
    
    def check_password(self):
        if self.username == "custom_auth_user" and self.password == "custom_auth_pass":
            return True
        return False


hide_registration = True if os.environ.get("HIDE_REGISTRATION") == "true" else False
hide_forgot_password = True if os.environ.get("HIDE_FORGOT_PASSWORD") == "true" else False
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
        custom_authentication = UserAuthTest(login_name="Test Login")
        custom_user_storage = UserStorageTest()
else:
    custom_user_storage = None

if os.environ.get("CUSTOM_FORGOT_PASSWORD") == "true":
    custom_forgot_password_msg = ForgotPasswordCustomMsgTest(message="Password via an insecure method")
else:
    custom_forgot_password_msg = None


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
    hide_forgot_password=hide_forgot_password,
    hide_account_management=hide_account_management,
    custom_authentication=custom_authentication,
    custom_user_storage=custom_user_storage,
    custom_forgot_password_msg=custom_forgot_password_msg
)


LOGGED_IN = __login__obj.build_login_ui()


if LOGGED_IN == True:
    st.markdown("Your Streamlit Application Begins here!")

    if st.button("Click here..."):
        st.write("Here is some more text.")