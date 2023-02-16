# src.handlers.user.py

from typing import Optional
from datetime import datetime
from argon2 import PasswordHasher
from sqlmodel import Session, select
from sqlalchemy.exc import NoResultFound
from src.apps.admin.models import User
from src.db.db import a_engine as engine


class SQLModelUserStorage:
    def register(
        self, name: str, email: str, username: str, password: str, first_name: str, last_name: str, ldap: bool = True
    ) -> None:
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
        ph = PasswordHasher()
        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            hashed_password=ph.hash(password),
            active=True,
            ldap=ldap,
            create_date=datetime.now(),
        )
        with Session(engine) as session:
            session.add(user)
            session.commit()

    def check_username_exists(self, username: str) -> bool:
        """
        Checks is username already exists in SQLModel database (SQLite)
        Args:
            username (str): username to check
        Return:
            bool: If username exists -> "True"; if not -> "False"
        """
        try:
            with Session(engine) as session:
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
            with Session(engine) as session:
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
        with Session(engine) as session:
            statement = select(User).where(User.email == email)
            if user := session.exec(statement).one():
                user.hashed_password = ph.hash(password)
                session.add(user)
                session.commit()
