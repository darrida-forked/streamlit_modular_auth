# src.handlers.cookies.py

import secrets
from datetime import datetime, timedelta
import streamlit as st
import diskcache


dc = diskcache.Cache("cache.db")


if show_typing := True:  # For typing purposes only
    from streamlit_modular_auth.protocols import CookieManager


class DiskcacheAuthCookies:
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

        if user_cache := dc.get(local_username):
            if (
                user_cache["auth_token"] == local_token
                and datetime.fromisoformat(user_cache["expires"]) >= datetime.now()
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
        auth_token = secrets.token_urlsafe(48)
        expires = datetime.now() + timedelta(seconds=200)
        user_session_cache = {"auth_token": auth_token, "expires": expires.isoformat()}
        dc.set(username, user_session_cache)
        cookies.set("auth_token", auth_token)
        cookies.set("auth_username", username)

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
        cookies.expire("groups")
        st.session_state.pop("groups")