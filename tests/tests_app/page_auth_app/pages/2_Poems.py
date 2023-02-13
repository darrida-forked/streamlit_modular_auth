import streamlit as st
from apps.poems.views import PoemsView


view = PoemsView()


st.title(view.title)


if not view.check_permissions():
    st.warning("Insufficient permissions")
else:
    view.check_state()

    st.write("[poems here]")

    st.write(view.state)
