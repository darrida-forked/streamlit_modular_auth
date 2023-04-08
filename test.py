# WORKING LOGIN SOLUTION
# - Works together with a NiceGUI login page that will be mounted to FastAPI

import json
from base64 import b64decode

import itsdangerous
import streamlit as st
from jose import JWTError, jwt
from loguru import logger
from streamlit.web.server.websocket_headers import _get_websocket_headers

if "try" not in st.session_state:
    st.session_state["try"] = 0
if st.session_state["try"] > 2:
    st.markdown('<a href="http://localhost:8000/login" target="_self">Open Login Page</a>', unsafe_allow_html=True)
    st.stop()

# This function can pull the websocket headers (including domain cookies) from the browser
headers = _get_websocket_headers()
st.write(headers)

# st.session_state["try"] += 1
# st.experimental_rerun()

# Parse "Cookie" header to get session cookie
cookies = headers.get("Cookie")
logger.info(cookies)
cookie_l = cookies.split(";")
cookie_l = [c.strip() for c in cookie_l]
logger.info(cookie_l)

session_l = [c for c in cookie_l if c.startswith("session")]
if len(session_l) == 0:
    st.experimental_rerun()
logger.info(session_l)
session = session_l[0].split("=", 1)
logger.info(f"session {session}")
st.write(f"session[1] {session[1]}")

# These 3 will need to be available to both entsys-fastapi and entsys-streamlit
FASTAPI_SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
FASTAPI_ALGORITHM = "HS256"
STARLETTE_MIDDLEWARE_SECRET = "some-random-string"

# Need to update entsys-fastapi to set this in a database, or somewhere that Streamlit can get to it
# session_info = {
#     '803c9bbd163eb61c0e25b97fda3d9e0c1c25fbc233d1b060b06451d2de230dfb9af61d97642e3b1426743d2e70f6cd1e': {
#         'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyIiwic2NvcGVzIjpbXSwiZXhwIjoxNjgwOTc5NjY2fQ.u2VZYlFBF4vqZfJW8LmxS6T9BGIFEYsdHaGGy9a8UVs',
#         'authenticated': True
#     }
# }
session_info = {
    "049a5efc58d78222909db07fbf4bddaa5f894b7bb54104bd7b26d5afe26a31f8ee1f9550bdfa4abdbb3d69bd760cbe8e": {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyIiwic2NvcGVzIjpbXSwiZXhwIjoxNjgwOTgxNTc3fQ.QMb2l92ftPfWyPjCQxja8Jef8Kbbs0JP5BEavO8IPMo",
        "authenticated": True,
    }
}

# This successfully decodes the session cookie to get the session id
signer = itsdangerous.TimestampSigner(STARLETTE_MIDDLEWARE_SECRET)
logger.info(session)
session = session[1]
data = session.encode("utf-8")
st.write(f"32: {data}")
data = signer.unsign(data, max_age=840000)
session_info_id = json.loads(b64decode(data))  # session_id = {"id": "<session_id>"}
st.write(f"35: {session_info_id}")

# Session id is used to get the access token from the session_info dict
if session_info_id["id"] in session_info:
    token = session_info[session_info_id["id"]]["access_token"]
payload = jwt.decode(token, FASTAPI_SECRET_KEY, algorithms=[FASTAPI_ALGORITHM])
st.write(payload)  # payload contains username, scopes/permissions, and expiration dates
