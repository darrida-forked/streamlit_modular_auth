import json
import os
from base64 import b64decode
from pathlib import Path

import itsdangerous
import streamlit as st
from jose import JWTError, jwt
from loguru import logger
from pydantic import BaseModel
from streamlit.web.server.websocket_headers import _get_websocket_headers

shared_config_file = Path(__file__).resolve().parent / ".config.json"
with open(shared_config_file) as f:
    shared_config = json.load(f)

FASTAPI_SECRET_KEY = os.environ.get("FASTAPI_SECRET_KEY") or shared_config["fastapi_secret_key"]
FASTAPI_ALGORITHM = os.environ.get("FASTAPI_ALGORITHM") or shared_config["fastapi_algorithm"]
STARLETTE_MIDDLEWARE_SECRET = (
    os.environ.get("STARLETTE_MIDDLEWARE_SECRET") or shared_config["starlette_middleware_secret"]
)
STARLETTE_MAX_AGE = os.environ.get("STARLETTE_MAX_AGE") or shared_config["starlette_expire_age"]


with open("/Users/ben/Documents/github/session_info.json") as f:
    session_info = json.load(f)


def get_session_cookie() -> str:
    if "get_cookie_attempt" not in st.session_state:
        st.session_state["get_cookie_attempt"] = 0

    headers = _get_websocket_headers()
    cookies = headers.get("Cookie")
    cookie_l = cookies.split(";")
    cookie_l = [c.strip() for c in cookie_l]
    session_l = [c for c in cookie_l if c.startswith("session")]

    logger.info(f"session_l: {session_l}")
    logger.info(st.session_state)
    if len(session_l) == 0:
        logger.info("No session cookie found")
        if st.session_state["get_cookie_attempt"] > 2:
            raise ValueError("No session cookie found")
        else:
            st.session_state["get_cookie_attempt"] += 1
            st.experimental_rerun()
    st.session_state.pop("get_cookie_attempt")
    session = session_l[0].split("=", 1)
    return session[1]


def decrypt_session_cookie(signed_session: str, max_age: int) -> str:
    signer = itsdangerous.TimestampSigner(STARLETTE_MIDDLEWARE_SECRET)
    try:
        data = signer.unsign(signed_value=signed_session.encode("utf-8"), max_age=max_age)
    except itsdangerous.SignatureExpired as e:
        raise itsdangerous.SignatureExpired(f"Attempted login with expired session cookie; {e}")
    except AttributeError as e:
        raise AttributeError(f"No session cookie to decrypt; {e}")
    return json.loads(b64decode(data))["id"]


def find_user_session(session_id: str) -> str:
    if session_id not in session_info:
        raise ValueError("Session not found")
    try:
        return session_info[session_id]["access_token"]
    except KeyError as e:
        raise KeyError(f"'access_token' not found in session record; {e}")


class AuthenticatedUser(BaseModel):
    username: str
    scopes: list
    expires: int


def check_authentication(token) -> AuthenticatedUser:
    try:
        session_d = jwt.decode(token, FASTAPI_SECRET_KEY, algorithms=[FASTAPI_ALGORITHM])
    except JWTError as e:
        raise JWTError(f"Invalid authentication token; {e}")
    return AuthenticatedUser(username=session_d["sub"], scopes=session_d["scopes"], expires=session_d["exp"])


def set_session_state(user: AuthenticatedUser):
    st.session_state["user"] = user


def nav_to(url):
    nav_script = """
        <meta http-equiv="refresh" content="0; url='%s'">
    """ % (
        url
    )
    st.write(nav_script, unsafe_allow_html=True)


def logged_in():
    try:
        signed_cookie = get_session_cookie()
        cookie = decrypt_session_cookie(signed_cookie, STARLETTE_MAX_AGE)
        token = find_user_session(cookie)
        if user := check_authentication(token):
            set_session_state(user)
            return True
    except (ValueError, JWTError, AttributeError, KeyError) as e:
        logger.info(f"No valid session found; redirecting to login page; error message: {e}")
        with st.spinner():
            st.button("Redirecting...", on_click=nav_to("http://localhost:8000/login"))
            st.stop()


if logged_in():
    st.write("You are logged in")
    st.write(st.session_state)
    st.write(st.session_state["user"].username)
    st.button("Logout", on_click=lambda: nav_to("http://localhost:8000/logout"))
