import streamlit as st

from streamlit_modular_auth import Login

login = Login()
logged_in = login.build_login_ui()


st.title("One session must be run without 'headless' mode to initialize sqlite database. This can be closed anytime.")


if logged_in is True:
    st.markdown("Your Streamlit Application Begins here!")

    if st.button("Click here..."):
        st.write("Here is some more text.")
