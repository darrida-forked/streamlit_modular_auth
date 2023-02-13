import streamlit as st
from streamlit_modular_auth import Login, config
from tests_handlers._test_forgot_password import ForgotPasswordCustomMsgTest


config.forgot_password_msg = ForgotPasswordCustomMsgTest(message="Password via an insecure method")
login_obj = Login()

logged_in = login_obj.build_login_ui()


if logged_in is True:
    st.markdown("Your Streamlit Application Begins here!")

    if st.button("Click here..."):
        st.write("Here is some more text.")
