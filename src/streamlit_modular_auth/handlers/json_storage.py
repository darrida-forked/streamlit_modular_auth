import json
from pathlib import Path
from typing import Optional
from datetime import datetime

from argon2 import PasswordHasher
import diskcache
import streamlit as st

dc = diskcache.Cache("cache.db")
ph = PasswordHasher()


class DefaultJSONUserAuth:
    def __init__(self, auth_filename: str = "_secret_auth_.json"):
        self.auth_filename = auth_filename

    def check_credentials(self, username, password) -> bool:
        """
        Authenticates using username and password class attributes.
        - Uses password and username from initialized object

        Return:
            bool: If password is correct -> "True"; if not -> "False"
        """
        with open(self.auth_filename, "r") as auth_json:
            authorized_user_data = json.load(auth_json)

        for user in authorized_user_data:
            if user["username"] == username and user["active"] is True:
                try:
                    if ph.verify(user["password"], password):
                        return True
                except Exception:
                    print("created better exception for _handlers.py line 34")
        return False


class DefaultJSONUserStorage:
    def __init__(self, auth_filename: str = "_secret_auth_.json"):
        self.auth_filename = auth_filename
        self.check_auth_json_file_exists()

    def register(self, first_name: str, last_name: str, email: str, username: str, password: str) -> None:
        """
        Saves the information of the new user in the json auth file.

        Args:
            name (str): name for new account
            email (str): email for new account
            username (str): username for new account
            password (str): password for new account

        Return:
            None
        """
        new_user = {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "active": True,
            "admin": False,
            "groups": [],
            "password": ph.hash(password),
            "created": datetime.now().isoformat(),
            "updated": "",
        }

        with open(self.auth_filename, "r") as auth_json:
            user_data = json.load(auth_json)

        if new_user["username"] in [x["username"] for x in user_data] or new_user["email"] in [
            x["email"] for x in user_data
        ]:
            st.write(f"Username {new_user['username']}, or {new_user['email']} already exists in storage")
            return

        with open(self.auth_filename, "w") as j:
            user_data.append(new_user)
            json.dump(user_data, j, indent=4)

    def check_username_exists(self, username: str) -> bool:
        """
        Checks if the username exists in the json auth file.

        Args:
            username (str): username to check

        Return:
            bool: If username exists -> "True"; if not -> "False"
        """
        authorized_user_data_master = list()
        with open(self.auth_filename, "r") as auth_json:
            authorized_users_data = json.load(auth_json)

            for user in authorized_users_data:
                authorized_user_data_master.append(user["username"])

        if username in authorized_user_data_master:
            return True
        return False

    def check_email_exists(self, email: str):
        """
        Checks if the email entered is present in the json auth file.

        Args:
            email (str): email connected to forgotten password

        Return:
            Tuple[bool, Optional[str]]: If exists -> (True, <username>); If not, (False, None)
        """
        with open(self.auth_filename, "r") as auth_json:
            authorized_users_data = json.load(auth_json)
            for user in authorized_users_data:
                if user["email"] == email:
                    return True, user["username"]
        return False, None

    def get_username_from_email(self, email: str) -> Optional[str]:
        """
        Retrieve username, if it exists, from the json auth file.

        Args:
            email (str): email connected to forgotten password

        Return:
            Optional[str]]: If exists -> <username>); If not -> None
        """
        with open(self.auth_filename, "r") as auth_json:
            authorized_users_data = json.load(auth_json)
        for user in authorized_users_data:
            if user["email"] == email:
                return user["username"]
        return None

    def change_password(self, email: str, password: str) -> None:
        """
        Replaces the old password with the newly generated password.

        Args:
            email (str): email connected to account
            password (str): password to set

        Return:
            None
        """
        with open(self.auth_filename, "r") as j_read:
            users_data = json.load(j_read)

        with open(self.auth_filename, "w") as j_write:
            for user in users_data:
                if user["email"] == email:
                    user["password"] = ph.hash(password)
                    user["updated"] = datetime.now().isoformat()
            json.dump(users_data, j_write, indent=4)

    def check_auth_json_file_exists(self) -> bool:
        """
        Checks if the auth file (where the user info is stored) already exists.
        """
        filename = Path(self.auth_filename)
        if not filename.exists():
            with open(filename, "w") as auth_json:
                json.dump([], auth_json)

    def init_storage(self):
        new_user = {
            "username": "admin",
            "first_name": "admin",
            "last_name": "admin",
            "email": "admin@no_email.com",
            "password": ph.hash("password11"),
            "active": True,
            "admin": True,
            "groups": [],
            "created": datetime.now().isoformat(),
            "updated": datetime.now().isoformat(),
        }

        with open(self.auth_filename, "r") as j_read:
            user_data = json.load(j_read)

        if new_user["username"] in [x["username"] for x in user_data]:
            print("`admin` username already exists in storage")
            return

        with open(self.auth_filename, "w") as j_write:
            user_data.append(new_user)
            json.dump(user_data, j_write, indent=4)


# class CourierForgotPasswordMsg:
#     def __init__(self, auth_token, company_name):
#         self.company_name = company_name
#         self.auth_token = auth_token

#     def send(self, username: str, email: str, reset_password: str) -> None:
#         """
#         Triggers an email to the user containing the randomly generated password.

#         Args:
#             auth_token (str): Courier api token
#             username (str): User's username
#             email (str): User's email
#             company_name (str): Used in email title ("<company_name>: Login Password")
#             reset_password (str): New temporary password to send

#         Returns:
#             None
#         """
#         client = Courier(auth_token=self.auth_token)

#         client.send_message(
#             message={
#                 "to": {"email": email},
#                 "content": {
#                     "title": self.company_name + ": Login Password!",
#                     "body": "Hi! "
#                     + username
#                     + ","
#                     + "\n"
#                     + "\n"
#                     + "Your temporary login password is: "
#                     + reset_password
#                     + "\n"
#                     + "\n"
#                     + "{{info}}",
#                 },
#                 "data": {"info": "Please reset your password at the earliest for security reasons."},
#             }
#         )
