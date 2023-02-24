from typing import TYPE_CHECKING, Optional

import diskcache
import streamlit as st
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, create_engine, select

from streamlit_modular_auth._apps.admin.models import User, create_db_and_tables, create_user

if TYPE_CHECKING:
    from sqlalchemy.engine import Engine

dc = diskcache.Cache("cache.db")
ph = PasswordHasher()


SQLITE_DEFAULT_URL = "sqlite:///sqlmodel_storage.sqlite"


engine = create_engine(SQLITE_DEFAULT_URL, pool_pre_ping=True)


class DefaultDBUserStorage:
    db: "Engine" = engine
    user: User

    def register(self, first_name: str, last_name: str, email: str, username: str, password: str) -> None:
        """
        Saves the information of the new user in SQLModel database (SQLite)
        Args:
            name (str): name for new account
            email (str): email for new account
            username (str): username for new account
            password (str): password for new account
        Return:
            None
        """
        User.create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            engine=self.db,
        )

    def check_username_exists(self, username: str) -> bool:
        """
        Checks is username already exists in SQLModel database (SQLite)
        Args:
            username (str): username to check
        Return:
            bool: If username exists -> "True"; if not -> "False"
        """
        try:
            with Session(self.db.connect()) as session:
                statement = select(User).where(User.username == username)
                if user := session.exec(statement).one():
                    print(user)
                    return True
        except NoResultFound:
            return False
        return False

    def get_username_from_email(self, email: str) -> Optional[str]:
        """
        Retrieve username, if it exists, from SQLModel database (SQLite) from provided email.
        Args:
            email (str): email connected to forgotten password
        Return:
            Optional[str]: If exists -> <username>; If not -> None
        """
        try:
            with Session(self.db.connect()) as session:
                statement = select(User).where(User.email == email)
                if user := session.exec(statement).one():
                    return user.username
        except NoResultFound:
            return None
        return None

    def change_password(self, email: str, password: str) -> None:
        """
        Replaces the old password in SQLModel database (SQLite) with the newly generated password.
        Args:
            email (str): email connected to account
            password (str): password to set
        Return:
            None
        """
        ph = PasswordHasher()
        with Session(self.db.connect()) as session:
            statement = select(User).where(User.email == email)
            if user := session.exec(statement).one():
                user.hashed_password = ph.hash(password)
                session.add(user)
                session.commit()

    def init_storage(self):
        create_db_and_tables(self.db)
        create_user(self.db)


class DefaultDBUserAuth(DefaultDBUserStorage):
    db: "Engine" = engine
    user: User

    def check_credentials(self, username, password):
        """
        Authenticates using username and password class attributes.
        - Uses password and username from initialized object
        - Queries user in SQLModel database (SQLite)
        - Checks password provided by streamlit_login_auth_ui against hashed password from database.
        Return:
            bool: If password is correct -> "True"; if not -> "False"
        """
        # MOVE AND GENERIALZE INTO PROTOCOL
        with Session(self.db.connect()) as session:
            st.write(username)
            statement = select(User).where(User.username == username)
            try:
                user = session.exec(statement).one()
                if user and user.active is True:
                    ph = PasswordHasher()
                    try:
                        if ph.verify(user.hashed_password, password):
                            if user.groups:
                                groups = [x.name for x in user.groups]
                                st.session_state["groups"] = groups
                            st.session_state["username"] = username
                            return True
                    except VerifyMismatchError as e:
                        if str(e) != "The password does not match the supplied hash":
                            raise VerifyMismatchError(e) from e
            except NoResultFound as e:
                if "No row was found" not in str(e):
                    raise NoResultFound(e) from e
        return False