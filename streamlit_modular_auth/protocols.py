from typing import Protocol, Optional
from streamlit_modular_auth._cookie_manager import CookieManager


class UserAuth(Protocol):
    def check_credentials(self, username, password) -> bool:
        """
        Authenticates using username and password class attributes.
        - Uses password and username from initialized object

        Return:
            bool: If password is correct -> "True"; if not -> "False"
        """
        ...


class UserStorage(Protocol):
    def register(self, name: str, email: str, username: str, password: str) -> None:
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

    def get_username_from_email(self, email: str) -> Optional[str]:
        """
        Retrieve username, if it exists, from user storage from provided email.

        Args:
            email (str): email connected to forgotten password

        Return:
            Optional[str]: If exists -> <username>; If not -> None
        """
        ...

    def change_password(self, email: str, password: str) -> None:
        """Replace password in user storage.

        Args:
            email (str): email connected to account
            password (str): password to set

        Return:
            None
        """
        ...


class ForgotPasswordMessage(Protocol):
    def send(self, username: str, email: str, reset_password: str) -> None:
        """Trigger an email to the user containing the randomly generated password.

        Args:
            username (str): User's username
            email (str): User's [TO:] email
            reset_password (str): New temporary password to send

        Returns:
            None
        """
        ...


class AuthCookies(Protocol):
    def check(self, cookies: CookieManager) -> bool:
        """
        Checks that auth cookies exist and are valid.
        - Exact internal setup isn't important, so long as it takes the specified parameter below, and
          validates existing cookies (if they exist)

        To Use:
        - Any logic here MUST include `cookies.get("<name>") to acquire the values to validate against
          - "<name>" must match the cookie name used in `self.cookie.set`
          - validate against the same data structure used in `self.cookie.set`

        Args:
            cookies (CookieManager): Initialized cookies manager provided by streamlit_login_auth_ui

        Returns:
            bool: If cookie(s) are valid -> True; if not valid -> False
        """
        ...

    def set(self, username, cookies: CookieManager) -> None:
        """
        Sets auth cookie using initialized EncryptedCookieManager.
        - Exact internal setup isn't important, so long as it takes the specified parameters,
          and sets cookies that indicate an authorized session, and can be interacted with by this class.

        To Use:
        - Any logic here MUST include `cookies.set("<name>", <value>)`
        - "<value>" can be of type STR or DICT

        Args:
            username (str): Authorized user
            cookies (CookieManager): Initialized cookies manager provided by streamlit_login_auth_ui

        Returns:
            None
        """
        ...

    def expire(self, cookies: CookieManager) -> None:
        """
        Expires auth cookie using initialized EncryptedCookieManager.
        - Exact internal setup isn't important, so long as it takes the specified parameters,
          and changes the existing cookies status to indicate an invalid session.

        To Use:
        - Any logic here MUST include `cookies.expire("<name>")`
        - "<name>" must match the cookie name used in `self.cookie.set`
        - Options:
          - When only a name is passed to `cookies.expire` the existing cookie is replaced with an empty string
          - A alternate value can also be passed using `cookies.expire("<name>", "<value")`, as long as it still
            results in an invalid check in `self.cookies.check`

        Args:
            cookies (CookieManager): Initialized cookies manager provided by streamlit_login_auth_ui

        Returns:
            None
        """
        ...
