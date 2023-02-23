import streamlit as st
from tests_handlers._test_user_storage import UserAuthTest, UserStorageTest

from streamlit_modular_auth import Login, ModularAuth

app = ModularAuth()
app.plugin_user_auth = UserAuthTest()
app.plugin_user_storage = UserStorageTest()
app.login_label = "Test Login"

login = Login(app)
logged_in = login.build_login_ui()

if logged_in is True:
    st.markdown("Your Streamlit Application Begins here!")

    if st.button("Click here..."):
        st.write("Here is some more text.")
