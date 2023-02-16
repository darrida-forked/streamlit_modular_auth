import streamlit as st
from apps.home import HomeView

from streamlit_modular_auth import Login

login = Login()


if login.build_login_ui():
    view = HomeView()
    st.write("got in")
    login.state["groups"] = ["page"]
    login.cookies.set("groups", "page")
    st.write(login.state)
else:
    st.write("not in")
    st.write(login.state)
