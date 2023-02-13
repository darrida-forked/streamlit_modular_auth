import streamlit as st
from streamlit_modular_auth import Login
from streamlit_modular_auth import config
from tests_handlers._test_user_storage import UserAuthTest, UserStorageTest


config.auth = UserAuthTest()
config.user_storage = UserStorageTest()

login_obj = Login(login_label="Test Login")
login_obj.setup(config)

logged_in = login_obj.build_login_ui()


if logged_in is True:
    st.markdown("Your Streamlit Application Begins here!")

    if st.button("Click here..."):
        st.write("Here is some more text.")
