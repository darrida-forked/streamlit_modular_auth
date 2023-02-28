from datetime import datetime
from typing import List, Optional

from argon2 import PasswordHasher
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlmodel import Field, Relationship, Session, SQLModel, select

ph = PasswordHasher()


class UserGroupsLink(SQLModel, table=True):
    __table_args__ = {
        # 'schema': "apps",
        "keep_existing": True,
        # 'extend_existing': True
    }

    group_id: Optional[int] = Field(default=None, foreign_key="streamlit_groups.id", primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="streamlit_users.id", primary_key=True)
    create_date: Optional[datetime] = datetime.now()
    created_by: str = "ADMIN"
    update_date: datetime = datetime.now()
    updated_by: str = "ADMIN"


class Group(SQLModel, table=True):
    __table_args__ = {
        # 'schema': "apps",
        "keep_existing": True,
        # 'extend_existing': True
    }
    __tablename__ = "streamlit_groups"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    active: bool = True
    create_date: datetime = datetime.now()
    created_by: str = "ADMIN"
    update_date: datetime = datetime.now()
    updated_by: str = "ADMIN"

    users: List["User"] = Relationship(back_populates="groups", link_model=UserGroupsLink)

    @staticmethod
    def get_all(engine: Engine) -> List["Group"]:
        with Session(engine.connect()) as session:
            statement = select(Group)
            groups = session.exec(statement)
            return list(groups)

    @staticmethod
    def create(name: str, engine: Engine):
        try:
            group = Group(name=name)
            with Session(engine.connect()) as session:
                session.add(group)
                session.commit()
        except IntegrityError as e:
            if "UNIQUE" not in str(e):
                raise IntegrityError(e) from e
            print(f"Group with name {group.name} already exists.")
            return False
        return True

    @staticmethod
    def set_status(status: bool, name: str, engine: Engine):
        with Session(engine.connect()) as session:
            statement = select(Group).where(Group.name == name)
            if group := session.exec(statement).one():
                group.active = status
                session.add(group)
                session.commit()
                return True
            else:
                return False
                # import streamlit as st
                # st.error("Found no record for group.")


class User(SQLModel, table=True):
    __table_args__ = {
        # 'schema': "apps",
        "keep_existing": True,
        # 'extend_existing': True
    }
    __tablename__ = "streamlit_users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    email: str = Field(unique=True)
    first_name: str
    last_name: str
    hashed_password: str
    active: bool
    admin: bool = False
    create_date: datetime = datetime.now()
    created_by: str = "ADMIN"
    update_date: datetime = datetime.now()
    updated_by: str = "ADMIN"

    groups: List[Group] = Relationship(back_populates="users", link_model=UserGroupsLink)

    @staticmethod
    def get(username: str = None, engine: Engine = None) -> "User":
        try:
            with Session(engine.connect()) as session:
                if username:
                    if user := _get_user(username, session):
                        return user
        except NoResultFound:
            pass
        return None

    @staticmethod
    def get_all(engine: Engine) -> List["User"]:
        with Session(engine.connect()) as session:
            statement = select(User)
            if users := session.exec(statement):
                return list(users)
        return None
        # import streamlit as st
        # st.error("Found no users.")

    @staticmethod
    def create(first_name: str, last_name: str, email: str, username: str, password: str, engine: Engine):
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
        )
        with Session(engine.connect()) as session:
            session.add(user)
            session.commit()

    @staticmethod
    def update(user: "User", engine: Engine) -> None:
        with Session(engine.connect()) as session:
            if saved_user := _get_user(user.username, session):
                saved_user.active = user.active
                saved_user.email = user.email
                saved_user.last_name = user.last_name
                saved_user.hashed_password = user.hashed_password
                saved_user.active = user.active
                # saved_user.ldap = user.ldap
                saved_user.admin = user.admin
            session.add(saved_user)
            session.commit()

    @staticmethod
    def get_groups(username: str, engine: Engine):
        with Session(engine.connect()) as session:
            if user := _get_user(username, session):
                return [x.name for x in user.groups] if user.groups else []
            else:
                return None
                # st.error("Found no record for user.")

    @staticmethod
    def add_group(username: str, groups: str, engine: Engine) -> None:
        with Session(engine.connect()) as session:
            group_statement = select(Group).where(Group.name == groups)
            group = session.exec(group_statement).one()
            if user := _get_user(username, session):
                user.groups.append(group)
                session.add(user)
                session.commit()
                return True
            else:
                return False
                # import streamlit as st
                # st.error("Found no record for user.")

    @staticmethod
    def delete_group(username: str, group: str, engine: Engine):
        with Session(engine.connect()) as session:
            group_statement = select(Group).where(Group.name == group)
            group = session.exec(group_statement).one()
            if user := _get_user(username, session):
                if user.groups:
                    user.groups.remove(group)
                    session.add(user)
                    session.commit()
                    return True
            else:
                return False
                # import streamlit as st
                # st.error("Found no record for user.")

    @staticmethod
    def set_status(status: bool, username: str, engine: Engine):
        with Session(engine.connect()) as session:
            if user := _get_user(username, session):
                user.active = status
                session.add(user)
                session.commit()
                return True
            else:
                return False
                # import streamlit as st
                # st.error("Found no record for user.")


def _get_user(username: str, session: Session) -> "User":
    user_statement = select(User).where(User.username == username)
    if user := session.exec(user_statement).one():
        return user
    return None

    # def _get_groups(self, username) -> Groups


def create_user(engine: Engine):
    from argon2 import PasswordHasher

    try:
        group = Group(name="admin")
        with Session(engine.connect()) as session:
            session.add(group)
            session.commit()
    except IntegrityError:
        print(f"Group named '{group.name}' already exists.")

    ph = PasswordHasher()
    try:
        user = User(
            username="admin",
            email="admin@no_email.com",
            first_name="admin",
            last_name="admin",
            hashed_password=ph.hash("password11"),
            active=True,
            admin=True,
        )
        with Session(engine.connect()) as session:
            if user.admin is True:
                statement = select(Group).where(Group.name == "admin")
                if admin_group := session.exec(statement).one():
                    user.groups.append(admin_group)
            session.add(user)
            session.commit()
    except IntegrityError:
        print(f"User with username {user.username} and/or email {user.email} already exists.")


def create_db_and_tables(engine):
    SQLModel.metadata.create_all(engine)
