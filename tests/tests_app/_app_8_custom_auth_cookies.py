import streamlit as st

# from streamlit_modular_auth import Login
# from streamlit_modular_auth import ModularAuth, DefaultPageView
from streamlit_modular_auth._core.modularauth import ModularAuth
from tests_handlers._test_cookies import UserAuthCookiesTest


app = ModularAuth()
app.plugin_auth_cookies = UserAuthCookiesTest()
app.login_expire = 15
app.login_label = "Test Login"

Login = app.login()
DefaultPageView = app.view()
DefaultPageModel = app.model()
login = Login()
view = DefaultPageView()


if login.build_login_ui() is True:
    st.markdown("Your Streamlit Application Begins here!")

    if st.button("Click here..."):
        st.write("Here is some more text.")

    if view.check_permissions():
        print("passed")
    else:
        print("not passed")
