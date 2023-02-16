# src.handlers.auth.py

from sqlmodel import Session, select
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import streamlit as st
from streamlit_modular_auth import cookies
from src.db.db import app_engine as engine
from src.apps.admin.models import User


class SQLModelUserAuth:
    def check_credentials(self, username, password):
        """
        Authenticates using username and password class attributes.
        - Uses password and username from initialized object
        - Queries user in SQLModel database (SQLite)
        - Checks password provided by streamlit_login_auth_ui against hashed password from database.
        Return:
            bool: If password is correct -> "True"; if not -> "False"
        """
        with Session(engine) as session:
            statement = select(User).where(User.username == username)
            user = session.exec(statement).one()
            if user and user.active is True:
                ph = PasswordHasher()
                try:
                    if self.ldap_auth(username, password) or ph.verify(  # Attempt to authenticate using LDAP
                        user.hashed_password, password
                    ):  # Attempt to authenticate using local password hash
                        if user.groups:
                            groups = [x.name for x in user.groups]
                            st.session_state["groups"] = groups
                            cookies.set("groups", ",".join(groups))
                        st.session_state["username"] = username
                        return True
                except VerifyMismatchError as e:
                    if str(e) != "The password does not match the supplied hash":
                        raise VerifyMismatchError(e) from e
        return False
