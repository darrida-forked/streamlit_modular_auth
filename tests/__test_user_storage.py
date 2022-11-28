from streamlit_login_auth_ui.utils import StreamlitUserStorage, StreamlitUserAuth
from streamlit_login_auth_ui.utils import ph


test_storage = [
    {
        "username": "user11",
        "name": "name11",
        "email": "email11@email.com",
        "hashed_password": ph.hash("password11")
    }
]


class StreamlitTestAuth(StreamlitUserAuth):
    def __init__(self, login_name=None, username=None, password=None):
        super().__init__(login_name, username, password)
    
    def check_usr_pass(self):
        user_l = [x for x in test_storage if x["username"] == self.username]
        if user_l:
            if ph.verify(user_l[0]["hashed_password"], self.password):
                return True
        return False


class StreamlitTestUserStorage(StreamlitUserStorage):
    storage_name: str = "sqlmodel"

    def check_unique_email(self, email_sign_up: str) -> bool:
        """
        Checks if the email already exists (since email needs to be unique).

        Args:
            email_sign_up (str): email for new account

        Return:
            bool: If email is unique -> "True"; if not -> "False"
        """
        user_l = [x for x in test_storage if x["email"] == email_sign_up]
        if user_l:
            return False
        return True

    def check_unique_usr(self, username_sign_up: str):
        """
        Checks if the username already exists (since username needs to be unique),
        also checks for non - empty username.

        Args:
            username_sign_up (str): username for new account

        Returns:
            bool: If username is unique -> "True"; if not -> "False"; if empty -> None
        """
        user_l = [x for x in test_storage if x["username"] == username_sign_up]
        if user_l:
            return False
        return True

    def register_new_usr(self, name_sign_up: str, email_sign_up: str, username_sign_up: str, password_sign_up: str) -> None:
        """
        Saves the information of the new user in the _secret_auth.json file.

        Args:
            name_sign_up (str): name for new account
            email_sign_up (str): email for new account
            username_sign_up (str): username for new account
            password_sign_up (str): password for new account

        Return:
            None
        """
        test_storage.append(
            {
                'username': username_sign_up,
                'name': name_sign_up,
                'email': email_sign_up,
                'hashed_password': ph.hash(password_sign_up)
            }
        )

    def check_username_exists(self, user_name: str) -> bool:
        """
        Checks if the username exists in the _secret_auth.json file.

        Args:
            user_name (str): username to check

        Return:
            bool: If username exists -> "True"; if not -> "False"
        """
        user_l = [x for x in test_storage if x["username"] == user_name]
        if user_l:
            return True
        return False

    def check_email_exists(self, email_forgot_passwd: str):
        """
        Checks if the email entered is present in the _secret_auth.json file.

        Args:
            email_forgot_passwd (str): email connected to forgotten password

        Return:
            Tuple[bool, Optional[str]]: If exists -> (True, <username>); If not, (False, None)
        """
        user_l = [x for x in test_storage if x["email"] == email_forgot_passwd]
        if user_l:
            return True, user_l[0]["username"]
        return False, None

    def change_passwd(self, email_: str, random_password: str) -> None:
        """
        Replaces the old password with the newly generated password.

        Args:
            email_ (str): email connected to account
            random_password (str): password to set

        Return:
            None
        """
        user_l = [x for x in test_storage if x["email"] == email_]
        if user_l:
            user_l[0]["hashed_password"] = ph.hash(random_password)

    def check_current_passwd(self, email_reset_passwd: str, current_passwd: str) -> bool:
        """
        Authenticates the password entered against the username when 
        resetting the password.

        Args:
            email_reset_passwd (str): email for account
            current_passwd (str): existing password for account
        
        Return:
            bool: If password is correct -> "True"; if not -> "False"
        """
        if not email_reset_passwd or not current_passwd:
            return False
        user_l = [x for x in test_storage if x["email"] == email_reset_passwd]
        if user_l:
            if ph.verify(user_l[0]["hashed_password"], current_passwd):
                return True
        return False
