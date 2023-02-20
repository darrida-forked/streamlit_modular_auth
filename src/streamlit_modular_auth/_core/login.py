from sys import argv
import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu

from streamlit_modular_auth._utils import (
    _check_valid_email,
    _check_valid_name,
    _check_valid_username,
    _generate_random_passwd,
    _load_lottieurl,
)
from streamlit_modular_auth.protocol_validation.auth import validate_user_auth
from streamlit_modular_auth.protocol_validation.auth_cookies import validate_auth_cookies
from streamlit_modular_auth.protocol_validation.storage import validate_user_storage

# from streamlit_modular_auth._apps.admin.models import init_database

from .config import ModularAuth


class Login:
    """Builds the UI for the Login/Sign Up page and manages all authentication logic."""

    def __init__(
        self,
        app: ModularAuth = None,
    ):
        if not app:
            app = ModularAuth()
        self.width = app.login_width
        self.height = app.login_height
        self.logout_button_name = app.logout_button_name
        self.hide_menu_bool = app.login_hide_menu
        self.hide_footer_bool = app.login_hide_footer
        self.lottie_url = app.login_lottie_url
        self.hide_registration = app.login_hide_registration
        self.hide_forgot_password = app.login_hide_forgot_password
        self.hide_account_management = app.login_hide_account_management
        self.login_label = app.login_label
        self.expire_delay = app.login_expire
        self.auth = app.plugin_user_auth
        self.storage = app.plugin_user_storage
        self.password_reset = app.plugin_forgot_password_msg
        self.auth_cookies = app.plugin_auth_cookies
        self.cookies = app.cookies
        self.state = app.state

        if "init_storage" in argv:
            self.storage.init_storage()
        if "check_user_storage" in argv:
            validate_user_storage(self.storage, self.auth)
        if "check_user_auth" in argv:
            validate_user_auth(self.auth, self.storage)
        if "check_auth_cookies" in argv:
            validate_auth_cookies(self.auth_cookies, self.cookies)

    def __login_widget(self) -> None:
        """
        Creates the login widget, checks and sets cookies, authenticates the users.
        """
        if st.session_state["LOGGED_IN"] is True:
            return

        if self.auth_cookies.check(self.cookies):
            st.session_state["LOGGED_IN"] = True
            return

        st.session_state["LOGOUT_BUTTON_HIT"] = False
        del_login = st.empty()
        with del_login.form("Login Form"):
            username = st.text_input("Username", placeholder="Your unique username")
            password = st.text_input("Password", placeholder="Your password", type="password")
            st.markdown("###")
            login_submit_button = st.form_submit_button(label="Login")

        if login_submit_button is True:
            if self.auth.check_credentials(username, password) is not True:
                st.error("Invalid Username or Password!")
            else:
                self.auth_cookies.set(username, self.cookies, self.expire_delay)
                if st.session_state.get("groups"):
                    groups = st.session_state["groups"]
                    self.cookies.set("groups", ",".join(groups))
                st.session_state["LOGGED_IN"] = True
                del_login.empty()
                st.experimental_rerun()

    def __animation(self) -> None:
        """
        Renders the lottie animation.
        """
        lottie_json = _load_lottieurl(self.lottie_url)
        st_lottie(lottie_json, width=self.width, height=self.height)

    def __sign_up_widget(self) -> None:
        """
        Creates the sign-up widget and stores the user info in a secure way in user storage.
        """
        with st.form("Sign Up Form"):
            first_name = st.text_input("First Name *", placeholder="Please enter your first name")
            last_name = st.text_input("Last Name *", placeholder="Please enter your last name")
            # name = st.text_input("Name *", placeholder="Please enter your name")
            email = st.text_input("Email *", placeholder="Please enter your email")
            username = st.text_input("Username *", placeholder="Enter a unique username")
            password = st.text_input("Password *", placeholder="Create a strong password", type="password")
            st.markdown("###")
            sign_up_submit_button = st.form_submit_button(label="Register")

        if sign_up_submit_button:
            if _check_valid_name(first_name) is False:
                st.error("Please enter a valid first name!")
            if _check_valid_name(last_name) is False:
                st.error("Please enter a valid last name!")
            elif _check_valid_email(email) is False:
                st.error("Please enter a valid Email!")
            elif _check_valid_username(username) is False:
                st.error("Please enter a valid Username! (no space characters)")
            elif self.storage.get_username_from_email(email):
                st.error("Email already exists!")
            elif self.storage.check_username_exists(username) is True:
                st.error("Sorry, username already exists!")
            else:
                self.storage.register(
                    first_name=first_name, last_name=last_name, email=email, username=username, password=password
                )
                st.success("Registration Successful!")

    def __forgot_password(self) -> None:
        """
        Creates the forgot password widget and after user authentication (email), triggers an email to the user
        containing a random password.
        """
        with st.form("Forgot Password Form"):
            email = st.text_input("Email", placeholder="Please enter your email")
            st.markdown("###")
            forgot_passwd_submit_button = st.form_submit_button(label="Get Password")

        if forgot_passwd_submit_button:
            if username := self.storage.get_username_from_email(email):
                random_password = _generate_random_passwd()
                self.password_reset.send(username, email, random_password)
                self.storage.change_password(email, random_password)
                st.success("Secure Password Sent Successfully!")
            else:
                st.error("No account with this email was found!")

    def __reset_password(self) -> None:
        """
        Creates the reset password widget and after user authentication (email and the password shared over that email),
        resets the password and updates the same in the user storage
        """
        with st.form("Reset Password Form"):
            email = st.text_input("Email", placeholder="Please enter your email")
            password = st.text_input("Temporary Password", placeholder="Please enter your current password")
            new_password = st.text_input(
                "New Password",
                placeholder="Please enter a new, strong password",
                type="password",
            )
            new_password_check = st.text_input(
                "Re - Enter New Password",
                placeholder="Please re- enter the new password",
                type="password",
            )
            st.markdown("###")
            reset_passwd_submit_button = st.form_submit_button(label="Reset Password")

        if reset_passwd_submit_button:
            username = self.storage.get_username_from_email(email)
            if not username:
                st.error("Email does not exist!")
            elif self.auth.check_credentials(username, password) is False:
                st.error("Incorrect password!")
            elif new_password != new_password_check:
                st.error("Passwords don't match!")
            else:
                self.storage.change_password(email, new_password_check)
                st.success("Password Reset Successfully!")

    def __logout_widget(self) -> None:
        """
        Creates the logout widget in the sidebar only if the user is logged in.
        """
        if st.session_state["LOGGED_IN"] is True:
            del_logout = st.sidebar.empty()
            del_logout.markdown("#")
            logout_click_check = del_logout.button(self.logout_button_name)

            if logout_click_check is True:
                st.session_state["LOGOUT_BUTTON_HIT"] = True
                self.auth_cookies.expire(self.cookies)
                st.session_state["LOGGED_IN"] = False
                del_logout.empty()
                st.experimental_rerun()

    def __nav_sidebar(self):
        """
        Creates the side navigaton bar
        """
        main_page_sidebar = st.sidebar.empty()
        with main_page_sidebar:
            icons = [
                "box-arrow-in-right",
                "person-plus",
                "x-circle",
                "arrow-counterclockwise",
            ]
            options = [
                self.login_label,
                "Create Account",
                "Forgot Password?",
                "Reset Password",
            ]
            if self.hide_registration or self.hide_account_management:
                icons.remove("person-plus")
                options.remove("Create Account")
            if self.hide_forgot_password or self.hide_account_management:
                icons.remove("x-circle")
                options.remove("Forgot Password?")
            if self.hide_account_management:
                icons.remove("arrow-counterclockwise")
                options.remove("Reset Password")
            selected_option = option_menu(
                menu_title="Navigation",
                menu_icon="list-columns-reverse",
                icons=icons,
                options=options,
                styles={
                    "container": {"padding": "5px"},
                    "nav-link": {
                        "font-size": "14px",
                        "text-align": "left",
                        "margin": "0px",
                    },
                },
            )
        return main_page_sidebar, selected_option

    def __hide_menu(self) -> None:
        """
        Hides the streamlit menu situated in the top right.
        """
        st.markdown(
            """ <style>
        #MainMenu {visibility: hidden;}
        </style> """,
            unsafe_allow_html=True,
        )

    def __hide_footer(self) -> None:
        """
        Hides the 'made with streamlit' footer.`
        """
        st.markdown(
            """ <style>
        footer {visibility: hidden;}
        </style> """,
            unsafe_allow_html=True,
        )

    def build_login_ui(self):
        """
        Brings everything together, calls important functions.
        """
        if "LOGGED_IN" not in st.session_state:
            st.session_state["LOGGED_IN"] = False

        if "LOGOUT_BUTTON_HIT" not in st.session_state:
            st.session_state["LOGOUT_BUTTON_HIT"] = False

        main_page_sidebar, selected_option = self.__nav_sidebar()

        if selected_option == self.login_label:
            c1, c2 = st.columns([7, 3])
            with c1:
                self.__login_widget()
            with c2:
                if st.session_state["LOGGED_IN"] is False:
                    self.__animation()

        if not self.hide_registration or not self.hide_account_management:
            if selected_option == "Create Account":
                self.__sign_up_widget()

        if not self.hide_forgot_password or not self.hide_account_management:
            if selected_option == "Forgot Password?":
                self.__forgot_password()

        if not self.hide_account_management:
            if selected_option == "Reset Password":
                self.__reset_password()

        self.__logout_widget()

        if st.session_state["LOGGED_IN"] is True:
            main_page_sidebar.empty()

        if self.hide_menu_bool is True:
            self.__hide_menu()

        if self.hide_footer_bool is True:
            self.__hide_footer()

        return st.session_state["LOGGED_IN"]


# Author: Gauri Prabhakar
# GitHub: https://github.com/GauriSP10/streamlit_login_auth_ui
