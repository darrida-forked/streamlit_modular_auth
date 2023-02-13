import streamlit as st
from apps.pictures.views import PicturesView


view = PicturesView()


st.title(view.title)


if not view.check_permissions():
    st.warning("Insufficient permissions")
else:
    view.check_state()

    st.write("[pictures here]")

    st.write(view.state)
