import streamlit as st
from apps.page1.views import Page1View


view = Page1View()
st.write(vars(view))


if not view.check_permissions():
    st.warning("Insufficient permissions")
    st.stop()

st.write("Got in to 1_Page")
