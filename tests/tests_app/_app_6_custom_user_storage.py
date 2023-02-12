import streamlit as st
from streamlit_modular_auth import Login
from tests_handlers._test_user_storage import UserAuthTest, UserStorageTest


login_obj = Login(
    auth_token="courier_auth_token",
    company_name="Sample Name",
    width=200,
    height=250,
    custom_login_label="Test Login",
    custom_authentication=UserAuthTest(),
    custom_user_storage=UserStorageTest(),
)


logged_in = login_obj.build_login_ui()


if logged_in is True:
    st.markdown("Your Streamlit Application Begins here!")

    if st.button("Click here..."):
        st.write("Here is some more text.")
