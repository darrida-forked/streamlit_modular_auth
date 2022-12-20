import streamlit as st
from streamlit_login_auth_ui import Login

login_obj = Login(auth_token = "courier_auth_token",
                    company_name = "Shims",
                    width = 200, height = 250,
                    logout_button_name = 'Logout', hide_menu_bool = False,
                    hide_footer_bool = False,
                    lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

logged_in = login_obj.build_login_ui()
username = login_obj.auth_cookies.get_username()

if logged_in == True:
   st.markdown("Your Streamlit Application Begins here!")
   st.markdown(st.session_state)
   st.write(username)
                                      
