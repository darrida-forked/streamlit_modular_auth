import streamlit as st

from apps.poems.views import PoemsView
from pages.base.config import app

view = PoemsView(app)


st.title(view.title)


if not view.check_permissions():
    st.warning("Insufficient permissions")
    st.stop()
else:
    view.check_state()
    st.write("[poems here]")
    st.write(view.state)
