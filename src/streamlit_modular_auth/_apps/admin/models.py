from datetime import datetime, timedelta
from typing import List, Optional

import requests
import streamlit as st
from argon2 import PasswordHasher
from loguru import logger
from pydantic import BaseModel

# from sqlmodel import Field, Relationship, Session, SQLModel, select

base_url = "http://localhost:8000"


ph = PasswordHasher()


def get_token():
    if "entsys-fastapi" in st.session_state:
        if st.session_state["entsys-fastapi"]["expires"] > datetime.now():
            return st.session_state["entsys-fastapi"]["token"]
    result = requests.post(
        url="http://localhost:8000/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        json={"username": "admin", "password": "admin"},
        timeout=10,
    )
    if result.status_code != 200:
        logger.warning(f"Unable to authenticate with entsys-fastapi API using {'admin'}.")

    token = result.json().get("access_token")
    expires = datetime.now() + timedelta(minutes=25)
    st.session_state["entsys-fastapi"] = {"token": token, "expires": expires}
    return token


class Group(BaseModel):
    name: str
    active: bool
    # create_date: datetime = datetime.now()
    # created_by: str = "ADMIN"
    # update_date: datetime = datetime.now()
    # updated_by: str = "ADMIN"

    # @staticmethod
    # def get_all(engine: Engine) -> List["Group"]:
    #     with Session(engine.connect()) as session:
    #         statement = select(Group)
    #         groups = session.exec(statement)
    #         return list(groups)

    @staticmethod
    def create(name: str):
        response = requests.post(url=f"{base_url}/maint/scope", json={"name": name, "disabled": True}, timeout=10)
        if response.status_code != 200:
            raise Exception(f"Error creating group: {response.status_code}; {response.text}")
        scope = response.json()
        group = Group(name=scope["name"], active=not scope["disabled"])
        if group.name == name:
            return True

    # @staticmethod
    # def set_status(status: bool, name: str, engine: Engine):
    #     with Session(engine.connect()) as session:
    #         statement = select(Group).where(Group.name == name)
    #         if group := session.exec(statement).one():
    #             group.active = status
    #             session.add(group)
    #             session.commit()
    #             return True
    #         else:
    #             return False
    #             # import streamlit as st
    #             # st.error("Found no record for group.")
    @staticmethod
    def delete(name: str):
        response = requests.delete(url=f"{base_url}/maint/scope", params={"scope": name}, timeout=10)
        if response.status_code != 200:
            raise Exception(f"Error deleting group: {response.status_code}; {response.text}")
        return True


class User(BaseModel):
    username: str
    email: str = None
    full_name: str = None
    password: str
    active: bool
    scopes: Optional[list] = []
    # admin: bool = False
    # create_date: datetime = datetime.now()
    # created_by: str = "ADMIN"
    # update_date: datetime = datetime.now()
    # updated_by: str = "ADMIN"

    @staticmethod
    def get(username: str = None) -> "User":
        token = get_token()
        response = requests.get(url="http://localhost:8000/maint/user", params={"username": username}, timeout=10)
        if response.status_code != 200:
            st.warning(f"Unable to retrieve user {username}.")
            st.stop()
        user = response.json()
        if user:
            logger.info(user)
            return User(
                username=user["username"],
                full_name=user["full_name"],
                email=user["email"],
                active=not user["disabled"],
                scopes=user["scopes"],
                password=user["password"],
            )
        return None

    @staticmethod
    def get_all() -> List["User"]:
        token = get_token()
        response = requests.get(url="http://localhost:8000/maint/users", timeout=10)
        if response.status_code != 200:
            st.warning("Unable to retrieve users.")
            st.stop()
        users = response.json()
        if users:
            logger.info(users)
            return [
                User(
                    username=x["username"],
                    full_name=x["full_name"],
                    email=x["email"],
                    active=not x["disabled"],
                    scopes=x["scopes"],
                    password=x["password"],
                )
                for x in users
            ]
        return None

    @staticmethod
    def create(full_name: str, email: str, username: str, password: str):
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
        token = get_token()
        response = requests.post(
            url="http://localhost:8000/maint/user",
            json={
                "username": username,
                "password": password,
                "full_name": full_name,
                "email": email,
                "disabled": False,
            },
            timeout=10,
        )
        if response.status_code != 200:
            raise Exception(f"Error creating user: {response.status_code}; {response.text}")
        user = response.json()
        return User(
            username=user["username"],
            email=user["email"],
            full_name=user["full_name"],
            password=user["password"],
            active=not user["disabled"],
        )

    @staticmethod
    def update(user: "User") -> "User":
        payload = {
            "username": user.username,
            "full_name": user.full_name,
            "email": user.email,
            "disabled": not user.active,
        }
        if user.password not in ("<hashed-passwoed>", "<hashed-password>"):
            payload["password"] = user.password

        token = get_token()
        response = requests.put(url="http://localhost:8000/maint/user", json=payload, timeout=10)
        if response.status_code != 200:
            raise Exception(f"Error updating user: {response.status_code}; {response.text}")
        user = response.json()
        return User(
            username=user["username"],
            full_name=user["full_name"],
            password=user["password"],
            active=not user["disabled"],
        )

    # @staticmethod
    # def get_groups(username: str, engine: Engine):
    #     with Session(engine.connect()) as session:
    #         if user := _get_user(username, session):
    #             return [x.name for x in user.groups] if user.groups else []
    #         else:
    #             return None
    # st.error("Found no record for user.")

    @staticmethod
    def add_group(username: str, group: str) -> bool:
        user = User.get(username)

        logger.info(user)
        logger.info(f"{username} + {group}")
        if group in user.scopes:
            raise ValueError(f"User {username} already has group {group}.")

        response = requests.post(
            url="http://localhost:8000/maint/user/scope", params={"username": username, "scope": group}, timeout=10
        )
        if response.status_code != 200:
            logger.error(response.status_code)
            logger.error(response.text)
            st.warning("Unable to enable user.")
            st.stop()

        user = User.get(username)
        if group in user.scopes:
            return True
        return False

        # scopes_before = set(user.scopes)

        # user.scopes.append(group)
        # updated_user = User.update(user)

        # scopes_after = set(updated_user.scopes)

        # if scopes_after.difference(scopes_before) == {group}:
        #     return True
        # return False

    @staticmethod
    def delete_group(username: str, group: str) -> bool:
        user = User.get(username)
        logger.info(user)
        logger.info(f"{username} - {group}")
        if group not in user.scopes:
            raise ValueError(f"User {username} does not have group {group}.")

        response = requests.delete(
            url="http://localhost:8000/maint/user/scope", params={"username": username, "scope": group}, timeout=10
        )
        if response.status_code != 200:
            logger.error(response.status_code)
            logger.error(response.text)
            st.warning("Unable to enable user.")
            st.stop()

        user = User.get(username)
        if group not in user.scopes:
            return True
        return False

    @staticmethod
    def set_status(status: bool, username: str):
        token = get_token()
        response = requests.put(
            url="http://localhost:8000/maint/user", json={"username": username, "disabled": status}, timeout=10
        )
        if response.status_code != 200:
            logger.error(response.status_code)
            logger.error(response.text)
            st.warning("Unable to enable user.")
            st.stop()
        return True


# def _get_user(username: str, session: Session) -> "User":
#     user_statement = select(User).where(User.username == username)
#     if user := session.exec(user_statement).one():
#         return user
#     return None

# def _get_groups(self, username) -> Groups


# def create_user(engine: Engine):
#     from argon2 import PasswordHasher

#     try:
#         group = Group(name="admin")
#         with Session(engine.connect()) as session:
#             session.add(group)
#             session.commit()
#     except IntegrityError:
#         print(f"Group named '{group.name}' already exists.")

#     ph = PasswordHasher()
#     try:
#         user = User(
#             username="admin",
#             email="admin@no_email.com",
#             first_name="admin",
#             last_name="admin",
#             hashed_password=ph.hash("password11"),
#             active=True,
#             admin=True,
#         )
#         with Session(engine.connect()) as session:
#             if user.admin is True:
#                 statement = select(Group).where(Group.name == "admin")
#                 if admin_group := session.exec(statement).one():
#                     user.groups.append(admin_group)
#             session.add(user)
#             session.commit()
#     except IntegrityError:
#         print(f"User with username {user.username} and/or email {user.email} already exists.")


# def create_db_and_tables(engine):
#     SQLModel.metadata.create_all(engine)
