import streamlit as st
from streamlit_modular_auth import Login, ModularAuth


app = ModularAuth()
app.login_hide_registration = True
login = Login(app)


st.markdown("## Streamlit Modular Auth")
st.markdown("### Hide Account Mangement")

st.warning(
    "Running the app in this mode means that you need to have an alternate means "
    "of creating and managing accounts. You could either use a workaround where "
    "you coule take one of two apporaches. (1) Worse case, you start the app with "
    "`login_hide_registration=False` "
    "to create accounts, then restart the app with `login_hide_registration=True` for usage. "
    "Or, *ideally*, (2) use this mode together with a custom `plugin_user_auth` handler, "
    "a custom `plugin_user_storage` handler, or a combination of both."
)


if login.build_login_ui():
    st.success("You're logged in!")
else:
    st.info("You're not logged in yet...")
