import secrets
from pathlib import Path
import json
from datetime import datetime, timedelta
import streamlit as st
from streamlit_login_auth_ui.protocols import CookieManager


class UserAuthCookiesTest:
    def __init__(self, auth_filename: str = "_secret_auth_.json"):
        self.auth_filename = auth_filename
        self.check_auth_json_file_exists()

    def check(self, cookies: CookieManager):
        """
        Checks that auth cookies exist and are valid.
        - Exact internal setup isn't important, so long as it takes the specified parameter below, and
          validates existing cookies (if they exist)

        Args:
            cookies (EncryptedCookieManager): Initialized cookies manager provided by streamlit_login_auth_ui

        Returns:
            bool: If cookie(s) are valid -> True; if not valid -> False
        """
        if "auth_username" not in cookies.keys() and "auth_token" in cookies.keys():
            return False
        local_username = cookies.get("auth_username")
        local_token = cookies.get("auth_token")

        with open(self.auth_filename, "r") as auth_json:
            json_user_storage = json.load(auth_json)

        for user in json_user_storage:
            if user.get("username") == local_username:
                if (
                    user["auth_session"]["auth_token"] == local_token
                    and datetime.fromisoformat(user["auth_session"]["expires"]) >= datetime.now()
                ):
                    return True
                else:
                    st.error("Session expired...")
        return False

    def set(self, username, cookies: CookieManager):
        """
        Sets auth cookie using initialized EncryptedCookieManager.
        - Exact internal setup isn't important, so long as it takes the specified parameters,
          and sets cookies that indicate an authorized session, and can be interacted with by this class.

        Args:
            username (str): Authorized user
            cookies (EncryptedCookieManager): Initialized cookies manager provided by streamlit_login_auth_ui

        Returns:
            None
        """

        with open(self.auth_filename, "r") as auth_json:
            json_user_storage = json.load(auth_json)

        auth_token = secrets.token_urlsafe(48)
        expires = datetime.now() + timedelta(seconds=15)
        for user in json_user_storage:
            if user.get("username") == username:
                user["auth_session"] = {
                    "auth_token": auth_token,
                    "expires": expires.isoformat(),
                }
                break
        cookies.set("auth_token", auth_token)
        cookies.set("auth_username", username)

        with open(self.auth_filename, "w") as auth_json_write:
            json.dump(json_user_storage, auth_json_write)

    def expire(self, cookies: CookieManager):
        """
        Expires auth cookie using initialized EncryptedCookieManager.
        - Exact internal setup isn't important, so long as it takes the specified parameters,
          and changes the existing cookies status to indicate an invalid session.

        Args:
            cookies (EncryptedCookieManager): Initialized cookies manager provided by streamlit_login_auth_ui

        Returns:
            None
        """
        cookies.expire("auth_token")

    def check_auth_json_file_exists(self) -> bool:
        """
        Checks if the auth file (where the user info is stored) already exists.
        """
        filename = Path(self.auth_filename)
        if not filename.exists():
            with open(filename, "w") as auth_json:
                json.dump([], auth_json)
