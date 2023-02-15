import streamlit as st
from streamlit_modular_auth import Login, ModularAuth
from tests_handlers._test_auth import CustomAuthTest


app = ModularAuth()
app.plugin_user_auth = CustomAuthTest()
app.login_hide_account_management = True

login = Login(app)
logged_in = login.build_login_ui()

if logged_in is True:
    st.markdown("Your Streamlit Application Begins here!")

    if st.button("Click here..."):
        st.write("Here is some more text.")
