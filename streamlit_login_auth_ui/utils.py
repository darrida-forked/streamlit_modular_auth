import re
import json
from trycourier import Courier
import secrets
from argon2 import PasswordHasher
import requests


ph = PasswordHasher() 


def load_lottieurl(url: str) -> str:
    """
    Fetches the lottie animation using the URL.
    """
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        pass


def check_valid_name(name_sign_up: str) -> bool:
    """
    Checks if the user entered a valid name while creating the account.
    """
    name_regex = (r'^[A-Za-z_][A-Za-z0-9_]*')

    if re.search(name_regex, name_sign_up):
        return True
    return False


def check_valid_email(email_sign_up: str) -> bool:
    """
    Checks if the user entered a valid email while creating the account.
    """
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

    if re.fullmatch(regex, email_sign_up):
        return True
    return False


def check_valid_username(username: str) -> bool:
    """
    Checks for username with no space characters
    """
    if not username:
        return False
    if " " in username:
        return False
    return True


def generate_random_passwd() -> str:
    """
    Generates a random password to be sent in email.
    """
    password_length = 10
    return secrets.token_urlsafe(password_length)


class DefaultUserAuth:
    def check_password(self, username, password) -> bool:
        """
        Authenticates using username and password class attributes.
        - Uses password and username from initialized object

        Return:
            bool: If password is correct -> "True"; if not -> "False"
        """
        with open("_secret_auth_.json", "r") as auth_json:
            authorized_user_data = json.load(auth_json)

        for user in authorized_user_data:
            if user['username'] == username:
                try:
                    passwd_verification_bool = ph.verify(user['password'], password)
                    if passwd_verification_bool == True:
                        return True
                except:
                    pass
        return False


class DefaultUserStorage:
    def register_new_usr(self, name: str, email: str, username: str, password: str) -> None:
        """
        Saves the information of the new user in the _secret_auth.json file.

        Args:
            name (str): name for new account
            email (str): email for new account
            username (str): username for new account
            password (str): password for new account

        Return:
            None
        """
        new_usr_data = {'username': username, 'name': name, 'email': email, 'password': ph.hash(password)}

        with open("_secret_auth_.json", "r") as auth_json:
            authorized_user_data = json.load(auth_json)

        with open("_secret_auth_.json", "w") as auth_json_write:
            authorized_user_data.append(new_usr_data)
            json.dump(authorized_user_data, auth_json_write)

    def check_username_exists(self, username: str) -> bool:
        """
        Checks if the username exists in the _secret_auth.json file.

        Args:
            username (str): username to check

        Return:
            bool: If username exists -> "True"; if not -> "False"
        """
        authorized_user_data_master = list()
        with open("_secret_auth_.json", "r") as auth_json:
            authorized_users_data = json.load(auth_json)

            for user in authorized_users_data:
                authorized_user_data_master.append(user['username'])
            
        if username in authorized_user_data_master:
            return True
        return False

    def check_email_exists(self, email: str):
        """
        Checks if the email entered is present in the _secret_auth.json file.

        Args:
            email (str): email connected to forgotten password

        Return:
            Tuple[bool, Optional[str]]: If exists -> (True, <username>); If not, (False, None)
        """
        with open("_secret_auth_.json", "r") as auth_json:
            authorized_users_data = json.load(auth_json)

            for user in authorized_users_data:
                if user['email'] == email:
                        return True, user['username']
        return False, None

    def change_passwd(self, email: str, password: str) -> None:
        """
        Replaces the old password with the newly generated password.

        Args:
            email (str): email connected to account
            password (str): password to set

        Return:
            None
        """
        with open("_secret_auth_.json", "r") as auth_json:
            authorized_users_data = json.load(auth_json)

        with open("_secret_auth_.json", "w") as auth_json_:
            for user in authorized_users_data:
                if user['email'] == email:
                    user['password'] = ph.hash(password)
            json.dump(authorized_users_data, auth_json_)


class DefaultForgotPasswordMsg:
    def send_password(self, auth_token: str, username: str, email: str, company_name: str, reset_password: str) -> None:
        """
        Triggers an email to the user containing the randomly generated password.

        Args:
            auth_token (str): Courier api token
            username (str): User's username
            email (str): User's email
            company_name (str): Used in email title ("<company_name>: Login Password")
            reset_password (str): New temporary password to send

        Returns:
            None
        """
        client = Courier(auth_token = auth_token)

        resp = client.send_message(
            message={
                "to": {
                "email": email
                },
                "content": {
                "title": company_name + ": Login Password!",
                "body": "Hi! " + username + "," + "\n" + "\n" + "Your temporary login password is: " + reset_password  + "\n" + "\n" + "{{info}}"
                },
                "data":{
                "info": "Please reset your password at the earliest for security reasons."
                }
            }
        )



# Author: Gauri Prabhakar
# GitHub: https://github.com/GauriSP10/streamlit_login_auth_ui
