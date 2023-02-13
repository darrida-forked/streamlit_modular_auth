from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, create_engine, Session, select
from argon2 import PasswordHasher
import streamlit as st
from sqlalchemy.exc import IntegrityError, NoResultFound

# from streamlit_modular_auth.protocols import UserStorage, UserAuth
from streamlit_modular_auth import Login


ph = PasswordHasher()


#######################################################################
# BOILERPLATE SPECIFIC TO SQLMODEL DATA (not the custom handler itself)
#######################################################################
class User(SQLModel, table=True):
    __table_args__ = {"keep_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    email: str = Field(unique=True)
    name: str
    hashed_password: str
    create_date: Optional[datetime]
    create_user: str = "administrator"
    update_date: datetime = datetime.now()
    update_user: str = "administrator"


def initialize_db_engine():
    sqlite_file_name = "sqlmodel_storage.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"
    return create_engine(sqlite_url)  # , echo=True)


engine = initialize_db_engine()


def create_db_and_tables(engine):
    SQLModel.metadata.create_all(engine)


def create_user(engine):
    try:
        user = User(
            username="user9",
            email="user9@email.com",
            name="flname",
            hashed_password=ph.hash("password9"),
        )
        with Session(engine) as session:
            session.add(user)
            session.commit()
    except IntegrityError as e:
        if "UNIQUE" not in str(e):
            raise IntegrityError(e) from e
        print(f"User with username {user.username} and/or email {user.email} already exists.")


def select_user(engine):
    try:
        with Session(engine) as session:
            statement = select(User).where(User.username == "user10")
            results = session.exec(statement).one()
            print(results)
        return True
    except NoResultFound:
        return False


#######################################################################
# CUSTOM HANDLERS
#######################################################################
class UserAuthSQLModel:
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
            if user:
                try:
                    if ph.verify(user.hashed_password, password):
                        return True
                except Exception:
                    print("Put better exception - dbmodule_storage.py like 95")
        return False


class UserStorageSQLModel:
    def register(self, name: str, email: str, username: str, password: str) -> None:
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
        user = User(username=username, email=email, name=name, hashed_password=ph.hash(password))
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
                user = session.exec(statement).one()
                if user:
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
                user = session.exec(statement).one()
                if user:
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
        with Session(engine) as session:
            statement = select(User).where(User.email == email)
            user = session.exec(statement).one()
            if user:
                user.hashed_password = ph.hash(password)
                session.add(user)
                session.commit()


if __name__ == "__main__":
    create_db_and_tables(engine)
    create_user(engine)
    select_user(engine)

    login_obj = Login(
        custom_authentication=UserAuthSQLModel(),
        custom_user_storage=UserStorageSQLModel(),
    )

    is_logged_in = login_obj.build_login_ui()

    if is_logged_in:
        st.markdown("Your Streamlit Application Begins here!")
