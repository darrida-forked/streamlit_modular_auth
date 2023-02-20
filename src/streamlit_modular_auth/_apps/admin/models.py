from datetime import datetime
from typing import List, Optional

from sqlalchemy.exc import IntegrityError
from sqlmodel import Field, Relationship, Session, SQLModel, select

from .db import engine


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


def create_user(engine):
    from argon2 import PasswordHasher

    try:
        group = Group(name="admin")
        with Session(engine) as session:
            session.add(group)
            session.commit()
    except IntegrityError as e:
        if "UNIQUE" not in str(e):
            raise IntegrityError(e) from e
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
        with Session(engine) as session:
            if user.admin is True:
                statement = select(Group).where(Group.name == "admin")
                if admin_group := session.exec(statement).one():
                    user.groups.append(admin_group)
            session.add(user)
            session.commit()
    except IntegrityError as e:
        if "UNIQUE" not in str(e):
            raise IntegrityError(e) from e
        print(f"User with username {user.username} and/or email {user.email} already exists.")


def create_db_and_tables(engine):
    SQLModel.metadata.create_all(engine)


def init_storage():
    create_db_and_tables(engine)
    create_user(engine)
