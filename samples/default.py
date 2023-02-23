import streamlit as st
from streamlit_modular_auth import Login

login = Login()


st.markdown("## Streamlit Modular Auth")
st.markdown("### Default Configuration")


if login.build_login_ui():
    st.success("You're logged in!")
