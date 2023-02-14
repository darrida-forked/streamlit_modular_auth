import streamlit as st
from streamlit_modular_auth import Login
from streamlit_modular_auth._base.config import config
from tests_handlers._test_cookies import UserAuthCookiesTest


config.auth_cookies = UserAuthCookiesTest()

login_obj = Login(login_label="Test Login", expire_delay=15)
login_obj.setup(config)


if login_obj.build_login_ui() is True:
    st.markdown("Your Streamlit Application Begins here!")

    if st.button("Click here..."):
        st.write("Here is some more text.")
