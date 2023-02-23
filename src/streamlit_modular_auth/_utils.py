import re
import secrets

import requests
from argon2 import PasswordHasher

ph = PasswordHasher()


def _load_lottieurl(url: str) -> str:
    """
    Fetches the lottie animation using the URL.
    """
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        print("create better exception for _utils.py line 20")


def _check_valid_name(name_sign_up: str) -> bool:
    """
    Checks if the user entered a valid name while creating the account.
    """
    name_regex = r"^[A-Za-z_][A-Za-z0-9_]*"

    if re.search(name_regex, name_sign_up):
        return True
    return False


def _check_valid_email(email_sign_up: str) -> bool:
    """
    Checks if the user entered a valid email while creating the account.
    """
    regex = re.compile(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+")

    if re.fullmatch(regex, email_sign_up):
        return True
    return False


def _check_valid_username(username: str) -> bool:
    """
    Checks for username with no space characters
    """
    if not username:
        return False
    if " " in username:
        return False
    return True


def _generate_random_passwd() -> str:
    """
    Generates a random password to be sent in email.
    """
    password_length = 10
    return secrets.token_urlsafe(password_length)


# Author: Gauri Prabhakar
# GitHub: https://github.com/GauriSP10/streamlit_login_auth_ui
