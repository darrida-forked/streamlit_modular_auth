from typing import Optional

from argon2 import PasswordHasher

ph = PasswordHasher()


test_storage = [
    {
        "username": "user11",
        "first_name": "name11",
        "last_name": "name22",
        "email": "email11@email.com",
        "hashed_password": ph.hash("password11"),
    }
]


class UserAuthTest:
    def check_credentials(self, username, password):
        user_l = [x for x in test_storage if x["username"] == username]
        if user_l:
            try:
                if ph.verify(user_l[0]["hashed_password"], password):
                    return True
            except Exception:
                print("create better exception for _test_user_storage.py line 26")
        return False


class UserStorageTest:
    def register(self, first_name: str, last_name: str, email: str, username: str, password: str) -> None:
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
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "hashed_password": ph.hash(password),
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
