from typing import Optional
from streamlit_login_auth_ui.utils import ph


test_storage = [
    {
        "username": "user11",
        "name": "name11",
        "email": "email11@email.com",
        "hashed_password": ph.hash("password11")
    }
]


class UserAuthTest:
    def check_password(self, username, password):
        user_l = [x for x in test_storage if x["username"] == username]
        if user_l:
            try:
                if ph.verify(user_l[0]["hashed_password"], password):
                    return True
            except:
                pass
        return False


class UserStorageTest:
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
        test_storage.append(
            {
                'username': username,
                'name': name,
                'email': email,
                'hashed_password': ph.hash(password)
            }
        )

    def check_username_exists(self, username: str) -> bool:
        """
        Checks if the username exists in the _secret_auth.json file.

        Args:
            username (str): username to check

        Return:
            bool: If username exists -> "True"; if not -> "False"
        """
        user_l = [x for x in test_storage if x["username"] == username]
        if user_l:
            return True
        return False

    # def check_email_exists(self, email: str):
    #     """
    #     Checks if the email entered is present in the _secret_auth.json file.

    #     Args:
    #         email (str): email connected to forgotten password

    #     Return:
    #         Tuple[bool, Optional[str]]: If exists -> (True, <username>); If not, (False, None)
    #     """
    #     user_l = [x for x in test_storage if x["email"] == email]
    #     if user_l:
    #         return True, user_l[0]["username"]
    #     return False, None

    def get_username_from_email(self, email: str) -> Optional[str]:
        user_l = [x for x in test_storage if x["email"] == email]
        if user_l:
            return user_l[0]["username"]
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
        user_l = [x for x in test_storage if x["email"] == email]
        if user_l:
            user_l[0]["hashed_password"] = ph.hash(password)
