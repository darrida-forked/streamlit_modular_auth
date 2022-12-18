from typing import Protocol, Optional


class UserAuth(Protocol):
    def check_password(self, username, password) -> bool:
        """
        Authenticates using username and password class attributes.
        - Uses password and username from initialized object

        Return:
            bool: If password is correct -> "True"; if not -> "False"
        """
        ...


class UserStorage(Protocol):
    def register_new_user(self, name: str, email: str, username: str, password: str) -> None:
        """
        Saves the information of the new user in user storage.

        Args:
            name (str): name for new account
            email (str): email for new account
            username (str): username for new account
            password (str): password for new account

        Return:
            None
        """
        ...

    def check_username_exists(self, username: str) -> bool:
        """
        Checks if the username exists in user storage.

        Args:
            username (str): username to check

        Return:
            bool: If username exists -> "True"; if not -> "False"
        """
        ...

    # def check_email_exists(self, email: str):
    #     """
    #     Checks if the email exists in user storage.

    #     Args:
    #         email (str): email connected to forgotten password

    #     Return:
    #         Tuple[bool, Optional[str]]: If exists -> (True, <username>); If not, (False, None)
    #     """
    #     ...

    def get_username_from_email(self, email: str) -> Optional[str]:
        """
        Retrieve username, if it exists, from user storage from provided email.

        Args:
            email (str): email connected to forgotten password

        Return:
            Optional[str]: If exists -> <username>; If not -> None
        """
        ...

    def change_passwd(self, email: str, password: str) -> None:
        """
        Replaces password in user storage.

        Args:
            email (str): email connected to account
            password (str): password to set

        Return:
            None
        """
        ...


class ForgotPasswordMessage(Protocol):
    def send_password(
        self, auth_token: str, username: str, email: str, company_name: str, reset_password: str
    ) -> None:
        """
        Triggers an email to the user containing the randomly generated password.

        Args:
            auth_token (str): api token
            username (str): User's username
            email (str): User's [TO:] email
            company_name (str): Used in message title ("<company_name>: Login Password")
            reset_password (str): New temporary password to send

        Returns:
            None
        """
        ...


