import streamlit as st

from streamlit_modular_auth import Login

# from streamlit_modular_auth import ModularAuth, DefauleBaseView
from streamlit_modular_auth import ModularAuth
from tests_handlers._test_cookies import UserAuthCookiesTest


app = ModularAuth()
app.plugin_auth_cookies = UserAuthCookiesTest()
app.login_expire = 15
app.login_label = "Test Login"

login = Login(app)

if login.build_login_ui() is True:
    st.markdown("Your Streamlit Application Begins here!")

    if st.button("Click here..."):
        st.write("Here is some more text.")
