# src.apps.admin.models.py

from typing import Optional, List
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship


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
    create_date: Optional[datetime]
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
    ldap: bool = True
    admin: bool = False
    create_date: Optional[datetime]
    created_by: str = "ADMIN"
    update_date: datetime = datetime.now()
    updated_by: str = "ADMIN"

    groups: List[Group] = Relationship(back_populates="users", link_model=UserGroupsLink)
