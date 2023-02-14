import streamlit as st
from streamlit_modular_auth import Login, ModularAuth
from tests_handlers._test_forgot_password import ForgotPasswordCustomMsgTest

forgot_msg = ForgotPasswordCustomMsgTest(message="Password via an insecure method")

app = ModularAuth()
app.plugin_forgot_password_msg = forgot_msg
login = Login(app)

logged_in = login.build_login_ui()

if logged_in is True:
    st.markdown("Your Streamlit Application Begins here!")

    if st.button("Click here..."):
        st.write("Here is some more text.")
