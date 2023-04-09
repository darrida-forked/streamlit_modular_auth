from typing import List, Optional, Union

from fastapi import HTTPException
from loguru import logger
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, ForeignKey, Table, select
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship

from src.database import db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


##############################################################
# FASTAPI MODELS
##############################################################
# ENDPOINT: CREATE USER
class APIUserAccount(BaseModel):
    username: str
    password: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    disabled: Optional[bool]
    scopes: list[str] = None


class APIUpdateAccount(BaseModel):
    username: str
    password: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class APIUserReturn(BaseModel):
    """Validation class and sample output to show in generated FastAPI documentation"""

    action: str
    user_info: APIUserAccount


# ENDPOINT: DELETE USERS
class APIUserDelete(BaseModel):
    result: str


class APIGroup(BaseModel):
    name: str
    disabled: Optional[bool] = None


##############################################################
# SQLALCHEMY DATABASE MODELS
##############################################################
enabled_access = Table(
    "user_access",
    db.Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("access_id", ForeignKey("access.id"), primary_key=True),
)


class DBUser(db.Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[Optional[str]]
    full_name: Mapped[Optional[str]]
    disabled: Mapped[bool] = mapped_column(default=False)
    hashed_password: Mapped[str]
    access: Mapped[List["DBAccess"]] = relationship(secondary=enabled_access, back_populates="user", lazy="joined")

    @staticmethod
    def create(api_user: APIUserAccount) -> APIUserReturn:
        user_email_stmt = stmt = select(DBUser).filter(
            (DBUser.username == api_user.username) | (DBUser.email == api_user.email)
        )
        user_stmt = select(DBUser).filter(DBUser.username == api_user.username)

        with Session(db.engine) as session:
            stmt = user_email_stmt if api_user.email else user_stmt
            if existing_user := session.execute(stmt).first():
                logger.warning(f"User already exists: {existing_user}")
                return

            db_user = DBUser(
                username=api_user.username,
                email=api_user.email,
                full_name=api_user.full_name,
                disabled=api_user.disabled,
                hashed_password=pwd_context.hash(api_user.password),
            )

            if api_user.scopes:
                access_stmt = select(DBAccess).filter(DBAccess.name.in_(api_user.scopes))
                access = session.execute(access_stmt).all()
                for a in access:
                    db_user.access.append(a[0])

            session.add(db_user)
            session.commit()
            new_user = session.execute(stmt).unique().one()

            new_user = new_user[0]
            if new_user.access:
                access_l = [n.name for n in new_user.access]
            else:
                access_l = None
            return APIUserReturn(
                action="CREATED",
                user_info=APIUserAccount(
                    username=new_user.username,
                    email=new_user.email,
                    full_name=new_user.full_name,
                    disabled=new_user.disabled,
                    scopes=access_l,
                    password="<converted-to-hashed-password>",  # noqa
                ),
            )

    @staticmethod
    def update(api_user: APIUpdateAccount) -> APIUpdateAccount:
        password_updated = False

        stmt = select(DBUser).filter(DBUser.username == api_user.username)
        with Session(db.engine) as session:
            db_user = session.execute(stmt).first()
            if not db_user:
                logger.warning(f"User not found: {api_user}")
                return

            db_user = db_user[0]
            if api_user.disabled is not None:
                db_user.disabled = api_user.disabled
            if api_user.full_name is not None:
                db_user.full_name = api_user.full_name
            if api_user.password is not None:
                password_updated = True
                db_user.hashed_password = pwd_context.hash(api_user.password)

            session.add(db_user)
            session.commit()
            updated_user = session.execute(stmt).unique()

            updated_user = updated_user[0]
            return APIUpdateAccount(
                username=updated_user.username,
                full_name=updated_user.full_name,
                disabled=updated_user.disabled,
                password="<password-hash-updated>" if password_updated is True else "<password-hash-unchanged>",
            )

    @staticmethod
    def remove_scope(username: str, scope: str):
        stmt_user = select(DBUser).filter(DBUser.username == username)
        stmt_scope = select(DBAccess).filter(DBAccess.name == scope)

        with Session(db.engine) as session:
            db_user = session.execute(stmt_user).first()
            if not db_user:
                logger.warning(f"User not found: {username}")
                raise HTTPException(status_code=403, detail="Existing user not found.")
            del_scope = session.execute(stmt_scope).first()
            db_user = db_user[0]
            try:
                db_user.access.remove(del_scope[0])
                session.add(db_user)
                session.commit()

                stmt_check = select(DBUser).where(DBUser.username == username)
                updated_user = session.execute(stmt_check).first()
                if scope in [u.name for u in updated_user[0].access]:
                    raise HTTPException(status_code=500, detail="Scope remove operation failed.")
            except ValueError as e:
                if "not in list" not in str(e):
                    raise ValueError(e) from e
                raise HTTPException(status_code=403, detail="Scope not found for user.")

    @staticmethod
    def add_scope(username: str, scope: str):
        stmt_user = select(DBUser).filter(DBUser.username == username)
        stmt_scope = select(DBAccess).filter(DBAccess.name == scope)

        with Session(db.engine) as session:
            db_user = session.execute(stmt_user).first()
            if not db_user:
                logger.warning(f"User not found: {username}")
                raise HTTPException(status_code=403, detail="Existing user not found.")

            if scope in [u.name for u in db_user[0].access]:
                raise HTTPException(status_code=403, detail="Scope already exists")

            add_scope = session.execute(stmt_scope).first()
            db_user = db_user[0]

            if add_scope[0].disabled is True:
                raise HTTPException(status_code=403, detail="Scope is disabled")
            db_user.access.append(add_scope[0])
            session.add(db_user)
            session.commit()

            stmt_check = select(DBUser).where(DBUser.username == username)
            updated_user = session.execute(stmt_check).first()
            if scope not in [u.name for u in updated_user[0].access]:
                raise HTTPException(status_code=500, detail="Scope add operation failed.")

    @staticmethod
    def delete(api_user: APIUserAccount) -> bool:
        stmt = select(DBUser).filter(DBUser.username == api_user.username)
        with Session(db.engine) as session:
            db_user = session.execute(stmt).first()
            if not db_user:
                return None

            session.delete(db_user[0])
            session.commit()
            if session.execute(stmt).first():
                return False
            return True

    @staticmethod
    def get_all(include_disabled: bool = False) -> list[APIUserAccount]:
        if include_disabled:
            stmt = select(DBUser).order_by(DBUser.username)
        else:
            stmt = select(DBUser).where(DBUser.disabled == False).order_by(DBUser.username)  # noqa
        with Session(db.engine) as session:
            db_users = session.execute(stmt).unique()

            return_l = []
            for u in db_users:
                u = u[0]
                if u.access:
                    access_l = [n.name for n in u.access]
                else:
                    access_l = None
                return_user = APIUserAccount(
                    username=u.username,
                    email=u.email,
                    full_name=u.full_name,
                    disabled=u.disabled,
                    scopes=access_l,
                    password="<hashed-passwoed>",  # noqa
                )
                return_l.append(return_user)
            return return_l

    @staticmethod
    def get(username: str, api_return: bool = False) -> Union["DBUser", APIUserAccount]:
        stmt = select(DBUser).where(DBUser.username == username)
        with Session(db.engine) as session:
            if db_user := session.execute(stmt).first():
                db_user = db_user[0]
                if not api_return:
                    return db_user
                if db_user.access:
                    access_l = [n.name for n in db_user.access]
                else:
                    access_l = None
                return APIUserAccount(
                    username=db_user.username,
                    email=db_user.email,
                    full_name=db_user.full_name,
                    disabled=db_user.disabled,
                    scopes=access_l,
                    password="<hashed-passwoed>",  # noqa
                )


class DBAccess(db.Base):
    __tablename__ = "access"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    disabled: Mapped[bool] = mapped_column(default=False)
    user: Mapped[List[DBUser]] = relationship(secondary=enabled_access, back_populates="access")

    @staticmethod
    def create(api_group: APIGroup) -> APIGroup:
        stmt = select(DBAccess).filter(DBAccess.name == api_group.name)

        with Session(db.engine) as session:
            if existing_group := session.execute(stmt).first():
                logger.warning(f"User already exists: {existing_group}")
                return

            db_access = DBAccess(name=api_group.name, disabled=api_group.disabled)
            session.add(db_access)
            session.commit()
            new_group = session.execute(stmt).one()

            new_group = new_group[0]
            return APIGroup(name=new_group.name, disabled=new_group.disabled)

    @staticmethod
    def delete(api_group: APIGroup):
        stmt = select(DBAccess).filter(DBAccess.name == api_group)
        with Session(db.engine) as session:
            db_scope = session.execute(stmt).first()
            if db_scope[0].user:
                raise HTTPException(status_code=403, detail="Delete note allowed; currently in use.")
            if not db_scope:
                return None

            session.delete(db_scope[0])
            session.commit()
            if session.execute(stmt).first():
                return False
            return True

    @staticmethod
    def get_all(include_disabled: bool = False) -> list["DBAccess"]:
        if include_disabled:
            stmt = select(DBAccess).order_by(DBAccess.name)
        else:
            stmt = select(DBAccess).where(DBAccess.disabled == False).order_by(DBAccess.name)  # noqa
        with Session(db.engine) as session:
            db_scopes = session.execute(stmt).unique()
            return list(db_scopes)
