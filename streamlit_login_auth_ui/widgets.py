import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
from streamlit_cookies_manager import EncryptedCookieManager
from icecream import ic
ic.configureOutput(includeContext=True)
from .utils import load_lottieurl
from .utils import check_valid_name
from .utils import check_valid_email
from .utils import generate_random_passwd
from .utils import DefaultUserAuth
from .utils import DefaultUserStorage
from .utils import DefaultForgotPasswordMsg
from .utils import check_valid_username


cookies = EncryptedCookieManager(
    prefix="auth_cookies",
    password='9d68d6f2-4258-45c9-96eb-2d6bc74ddbb5-d8f49cab-edbb-404a-94d0-b25b1d4a564b'
)

if not cookies.ready():
    st.stop() 


class __login__:
    """
    Builds the UI for the Login/ Sign Up page.
    """

    def __init__(self, auth_token: str, company_name: str, width: int, height: int, logout_button_name: str = 'Logout',
                 hide_menu_bool: bool = False, hide_footer_bool: bool = False, 
                 lottie_url: str = "https://assets8.lottiefiles.com/packages/lf20_ktwnwv5m.json",
                 hide_registration: bool = False, hide_account_management: bool = False, 
                 hide_forgot_password: bool = False,
                 custom_login_label: str = None,
                 custom_authentication: DefaultUserAuth = None,
                 custom_user_storage: DefaultUserStorage = None,
                 custom_forgot_password_msg: DefaultForgotPasswordMsg = None):
        """
        Arguments:
        -----------
        1. self
        2. auth_token : The unique authorization token received from - https://www.courier.com/email-api/
        3. company_name : This is the name of the person/ organization which will send the password reset email.
        4. width : Width of the animation on the login page.
        5. height : Height of the animation on the login page.
        6. logout_button_name : The logout button name.
        7. hide_menu_bool : Pass True if the streamlit menu should be hidden.
        8. hide_footer_bool : Pass True if the 'made with streamlit' footer should be hidden.
        9. lottie_url : The lottie animation you would like to use on the login page. Explore animations at - https://lottiefiles.com/featured
        10. hide_registration : Pass True if 'Create Account' option should be hidden from Navigation.
        11. hide_forgot_password : Pass True if 'Forgot Password?' option should be hidden from Navigation.
        11. hide_account_management : Pass True if all options other than 'Login' should be hidden from Navigation.
        12. custom_authentication : Option to pass custom authentication class that inherits from StreamlitDefaultUserAuth (see information further below).
        13. custom_user_storage : Option to pass custom user storage class that inherits from StreamLitDefaultUserStorage (see information further below).
        """
        self.auth_token = auth_token
        self.company_name = company_name
        self.width = width
        self.height = height
        self.logout_button_name = logout_button_name
        self.hide_menu_bool = hide_menu_bool
        self.hide_footer_bool = hide_footer_bool
        self.lottie_url = lottie_url
        self.hide_registration = hide_registration
        self.hide_forgot_password = hide_forgot_password
        self.hide_account_management = hide_account_management
        self.login_label = custom_login_label or "Login"
        self.auth = custom_authentication or DefaultUserAuth()
        self.storage = custom_user_storage or DefaultUserStorage()
        self.password_reset = custom_forgot_password_msg or DefaultForgotPasswordMsg()


    def get_username(self):
        if st.session_state['LOGOUT_BUTTON_HIT'] == False:
            fetched_cookies = cookies
            if '__streamlit_login_signup_ui_username__' in fetched_cookies.keys():
                username=fetched_cookies['__streamlit_login_signup_ui_username__']
                return username
 

    def check_auth_cookie(self):
        if '__streamlit_login_signup_ui_username__' in cookies.keys() and st.session_state['LOGOUT_BUTTON_HIT'] == False:
            if cookies.get('__streamlit_login_signup_ui_username__') == 'ben': # self.storage.hashed_cookie(extend=True)
                st.session_state['LOGGED_IN'] = True
                return True
        return False


    def set_auth_cookie(self, username):
        cookies['__streamlit_login_signup_ui_username__'] = username
        cookies.save()


    def expire_auth_cookie(self):
        cookies['__streamlit_login_signup_ui_username__'] = ""
        cookies.save()


    def login_widget(self) -> None:
        """
        Creates the login widget, checks and sets cookies, authenticates the users.
        """
        if st.session_state["LOGGED_IN"] == True:
            return

        if self.check_auth_cookie():
            return
        
        st.session_state['LOGOUT_BUTTON_HIT'] = False
        del_login = st.empty()
        with del_login.form("Login Form"):
            username = st.text_input("Username", placeholder = 'Your unique username')
            password = st.text_input("Password", placeholder = 'Your password', type = 'password')
            st.markdown("###")
            login_submit_button = st.form_submit_button(label = 'Login')

        if login_submit_button == True:
            if self.auth.check_password(username, password) != True:
                st.error("Invalid Username or Password!")
            else:
                self.set_auth_cookie(username)
                st.session_state["LOGGED_IN"] = True
                del_login.empty()
                st.experimental_rerun()


    def animation(self) -> None:
        """
        Renders the lottie animation.
        """
        lottie_json = load_lottieurl(self.lottie_url)
        st_lottie(lottie_json, width = self.width, height = self.height)


    def sign_up_widget(self) -> None:
        """
        Creates the sign-up widget and stores the user info in a secure way in user storage.
        """
        with st.form("Sign Up Form"):
            name = st.text_input("Name *", placeholder = 'Please enter your name')
            email = st.text_input("Email *", placeholder = 'Please enter your email')
            username = st.text_input("Username *", placeholder = 'Enter a unique username')
            password = st.text_input("Password *", placeholder = 'Create a strong password', type = 'password')
            st.markdown("###")
            sign_up_submit_button = st.form_submit_button(label = 'Register')

        if sign_up_submit_button:
            if check_valid_name(name) == False:
                st.error("Please enter a valid name!")
            elif check_valid_email(email) == False:
                st.error("Please enter a valid Email!")
            elif check_valid_username(username) == False:
                st.error('Please enter a valid Username! (no space characters)')
            elif self.storage.get_username_from_email(email):
                st.error("Email already exists!")
            elif self.storage.check_username_exists(username) == True:
                st.error('Sorry, username already exists!')
            else:
                self.storage.register_new_usr(name, email, username, password)
                st.success("Registration Successful!")


    def forgot_password(self) -> None:
        """
        Creates the forgot password widget and after user authentication (email), triggers an email to the user 
        containing a random password.
        """
        with st.form("Forgot Password Form"):
            email = st.text_input("Email", placeholder= 'Please enter your email')
            st.markdown("###")
            forgot_passwd_submit_button = st.form_submit_button(label = 'Get Password')

        if forgot_passwd_submit_button:
            if username := self.storage.get_username_from_email(email):
                random_password = generate_random_passwd()
                self.password_reset.send_password(self.auth_token, username, email, self.company_name, random_password)
                self.storage.change_passwd(email, random_password)
                st.success("Secure Password Sent Successfully!")
            else:
                st.error("No account with this email was found!")


    def reset_password(self) -> None:
        """
        Creates the reset password widget and after user authentication (email and the password shared over that email), 
        resets the password and updates the same in the user storage
        """
        with st.form("Reset Password Form"):
            email = st.text_input("Email", placeholder= 'Please enter your email')
            password = st.text_input("Temporary Password", placeholder= 'Please enter your current password')
            new_password = st.text_input("New Password", placeholder= 'Please enter a new, strong password', type = 'password')
            new_password_check = st.text_input("Re - Enter New Password", placeholder= 'Please re- enter the new password', type = 'password')
            st.markdown("###")
            reset_passwd_submit_button = st.form_submit_button(label = 'Reset Password')

        if reset_passwd_submit_button:
            username = self.storage.get_username_from_email(email)
            if not username:
                st.error("Email does not exist!")
            elif self.auth.check_password(username, password) == False:
                st.error("Incorrect password!")
            elif new_password != new_password_check:
                st.error("Passwords don't match!")
            else:
                self.storage.change_passwd(email, new_password_check)
                st.success("Password Reset Successfully!")
                

    def logout_widget(self) -> None:
        """
        Creates the logout widget in the sidebar only if the user is logged in.
        """
        if st.session_state['LOGGED_IN'] == True:
            del_logout = st.sidebar.empty()
            del_logout.markdown("#")
            logout_click_check = del_logout.button(self.logout_button_name)

            if logout_click_check == True:
                st.session_state['LOGOUT_BUTTON_HIT'] = True
                self.expire_auth_cookie()
                st.session_state['LOGGED_IN'] = False
                del_logout.empty()
                st.experimental_rerun()
        

    def nav_sidebar(self):
        """
        Creates the side navigaton bar
        """
        main_page_sidebar = st.sidebar.empty()
        with main_page_sidebar:
            icons = ['box-arrow-in-right', 'person-plus', 'x-circle','arrow-counterclockwise']
            options = [self.login_label, 'Create Account', 'Forgot Password?', 'Reset Password']
            if self.hide_registration or self.hide_account_management:
                icons.remove('person-plus')
                options.remove('Create Account')
            if self.hide_forgot_password or self.hide_account_management:
                icons.remove('x-circle')
                options.remove('Forgot Password?')
            if self.hide_account_management:
                icons.remove('arrow-counterclockwise')
                options.remove('Reset Password')
            selected_option = option_menu(
                menu_title = 'Navigation',
                menu_icon = 'list-columns-reverse',
                icons = icons,
                options = options,
                styles = {
                    "container": {"padding": "5px"},
                    "nav-link": {"font-size": "14px", "text-align": "left", "margin":"0px"}} )
        return main_page_sidebar, selected_option
    

    def hide_menu(self) -> None:
        """
        Hides the streamlit menu situated in the top right.
        """
        st.markdown(""" <style>
        #MainMenu {visibility: hidden;}
        </style> """, unsafe_allow_html=True)
    

    def hide_footer(self) -> None:
        """
        Hides the 'made with streamlit' footer.
        """
        st.markdown(""" <style>
        footer {visibility: hidden;}
        </style> """, unsafe_allow_html=True)


    def build_login_ui(self):
        """
        Brings everything together, calls important functions.
        """
        if 'LOGGED_IN' not in st.session_state:
            st.session_state['LOGGED_IN'] = False

        if 'LOGOUT_BUTTON_HIT' not in st.session_state:
            st.session_state['LOGOUT_BUTTON_HIT'] = False

        main_page_sidebar, selected_option = self.nav_sidebar()

        if selected_option == self.login_label:
            c1, c2 = st.columns([7,3])
            with c1:
                self.login_widget()
            with c2:
                if st.session_state['LOGGED_IN'] == False:
                    self.animation()
        
        if not self.hide_registration or not self.hide_account_management:
            if selected_option == 'Create Account':
                self.sign_up_widget()

        if not self.hide_forgot_password or not self.hide_account_management:
            if selected_option == 'Forgot Password?':
                self.forgot_password()

        if not self.hide_account_management:
            if selected_option == 'Reset Password':
                self.reset_password()
        
        self.logout_widget()

        if st.session_state['LOGGED_IN'] == True:
            main_page_sidebar.empty()
        
        if self.hide_menu_bool == True:
            self.hide_menu()
        
        if self.hide_footer_bool == True:
            self.hide_footer()
        
        return st.session_state['LOGGED_IN']

# Author: Gauri Prabhakar
# GitHub: https://github.com/GauriSP10/streamlit_login_auth_ui


