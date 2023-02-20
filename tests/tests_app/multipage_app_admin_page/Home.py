import streamlit as st
from apps.home.views import HomeView
from pages.base.config import app

from streamlit_modular_auth import Login


login = Login(app)
logged_in = login.build_login_ui()


if logged_in is True:
    view = HomeView(app)
    view.check_state()

    st.markdown("Your Streamlit Application Begins here!")

    if st.button("Add Poems"):
        view.state["groups"].append("poems")
        view.cookies.set("groups", ",".join(view.state["groups"]))
        st.write("Permissions for poems group added")

    st.write(view.state)
    if view.state["page"]["name"] == "home":
        st.info("Home page state set")
