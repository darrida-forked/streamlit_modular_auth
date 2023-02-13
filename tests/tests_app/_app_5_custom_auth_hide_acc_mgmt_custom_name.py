import streamlit as st
from streamlit_modular_auth import Login, config
from tests_handlers._test_auth import CustomAuthTest


config.auth = CustomAuthTest()
login_obj = Login(hide_account_management=True, login_label="Custom Login")
login_obj.setup(config)

logged_in = login_obj.build_login_ui()


if logged_in is True:
    st.markdown("Your Streamlit Application Begins here!")

    if st.button("Click here..."):
        st.write("Here is some more text.")
