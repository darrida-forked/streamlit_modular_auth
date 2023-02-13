import os
from typing import Any
import secrets
import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager


class CookieManager:
    """Front-end to EncryptedCookieManager
    - Abstracting third-party cookie manager commands behind a local implementation makes custom
      auth cookie interaction possible while also allowing the actual cookie manager used to
      be changed in the future, if required.

    To Use:
    - If looking to impliment custom auth cookie logic/structure, instead see
      `streamlit_modular_auth.protocols.AuthCookies`.
    - If looking to interact with cookies in other ways, import `streamlit_modular_auth.cookies`
    """

    def __init__(self, cookies: EncryptedCookieManager):
        self.cookies = cookies

    def get(self, name) -> Any:
        return self.cookies.get(name)

    def set(self, name, val) -> None:
        self.cookies[name] = val
        # self.cookies.save()

    def expire(self, name: str, val: Any = None) -> None:
        if not val:
            val = ""
        self.cookies[name] = val

    def keys(self):
        return self.cookies.keys()


def _initialize_cookie_manbager() -> CookieManager:
    prefix = os.environ.get("ALT_AUTH_COOKIE_PREFIX") or "auth_cookies"  # Makes robot_tests easier
    cookies = EncryptedCookieManager(prefix=prefix, password=secrets.token_urlsafe(48))
    if not cookies.ready():
        st.stop()
    return CookieManager(cookies)
