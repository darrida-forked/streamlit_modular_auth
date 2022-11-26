import os
import streamlit as st
from streamlit_login_auth_ui import __login__


hide_registration = True if os.environ.get("HIDE_REGISTRATION") == "true" else False
hide_account_management = True if os.environ.get("HIDE_ACCOUNT_MANAGEMENT") == "true" else False
hide_footer_bool = True if os.environ.get("HIDE_FOOTER") == "true" else False
hide_menu_bool = True if os.environ.get("HIDE_MENU") == "true" else False
logout_button_name = True if os.environ.get("LOGOUT_BUTTON_NAME") == "true" else False


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
    hide_account_management=hide_account_management
)


LOGGED_IN = __login__obj.build_login_ui()


if LOGGED_IN == True:
    st.markdown("Your Streamlit Application Begins here!")