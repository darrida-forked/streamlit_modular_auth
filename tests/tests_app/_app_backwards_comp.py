import streamlit as st
from streamlit_modular_auth import __login__


__login__obj = __login__(
    auth_token="courier_auth_token",
    company_name="Shims",
    width=200,
    height=250,
    logout_button_name="Logout",
    hide_menu_bool=False,
    hide_footer_bool=False,
    lottie_url="https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json",
)


logged_in = __login__obj.build_login_ui()
username = __login__obj.get_username()


if logged_in is True:
    st.markdown("Your Streamlit Application Begins here!")
    st.markdown(st.session_state)
    st.write(username)
