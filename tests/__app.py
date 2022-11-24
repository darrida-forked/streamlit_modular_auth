import streamlit as st
from streamlit_login_auth_ui import __login__


__login__obj = __login__(
    auth_token = "courier_auth_token", 
    company_name = "Waubonsee",
    width = 200, height = 250, 
    logout_button_name = 'Logout', hide_menu_bool = False, 
    hide_footer_bool = True, 
    lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json'
)


LOGGED_IN = __login__obj.build_login_ui()

if LOGGED_IN == True:
    st.markdown("Your Streamlit Application Begins here!")


# import streamlit as st

# st.title("Test")
# genre = st.radio(
#     "What's your favorite movie genre",
#     ('Comedy', 'Drama', 'Documentary'))

# if genre == 'Comedy':
#     st.write('You selected comedy.')
# else:
#     st.write("You didn't select comedy.")