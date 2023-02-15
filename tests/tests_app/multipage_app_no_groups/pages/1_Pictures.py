import streamlit as st
from pages.base.config import app
from apps.pictures.views import PicturesView


view = PicturesView(app)


st.title(view.title)


if not view.check_permissions():
    st.warning("Insufficient permissions")
else:
    view.check_state()
    st.write("[pictures here]")
    st.write(view.state)
    if view.state["page"]["name"] == "pictures":
        st.info("Picture page state set")