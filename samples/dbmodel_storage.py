from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, create_engine, Session, select
from sqlalchemy.exc import IntegrityError, NoResultFound
from streamlit_login_auth_ui.utils import ph, StreamlitUserStorage, StreamlitUserAuth


class User(SQLModel, table=True):
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
    return create_engine(sqlite_url)#, echo=True)


engine = initialize_db_engine()


def create_db_and_tables(engine):
    SQLModel.metadata.create_all(engine)


def create_user(engine):
    try:
        user = User(
            username="user9",
            email="user9@email.com",
            name="flname",
            hashed_password=ph.hash("password9")
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


class StreamLitSQLModelAuth(StreamlitUserAuth):
    def __init__(self, login_name=None, username=None, password=None):
        super().__init__(login_name, username, password)
    
    def check_password(self):
        with Session(engine) as session:
            statement = select(User).where(User.username == self.username)
            user = session.exec(statement).one()
            if user:
                if ph.verify(user.hashed_password, self.password):
                    return True
        return False


class StreamLiteSQLModelStorage(StreamlitUserStorage):
    storage_name: str = "sqlmodel"

    def register_new_usr(self, name_sign_up: str, email_sign_up: str, username_sign_up: str, password_sign_up: str) -> None:
        """
        Saves the information of the new user in the _secret_auth.json file.

        Args:
            name_sign_up (str): name for new account
            email_sign_up (str): email for new account
            username_sign_up (str): username for new account
            password_sign_up (str): password for new account

        Return:
            None
        """
        user = User(
            username=username_sign_up,
            email=email_sign_up,
            name=name_sign_up,
            hashed_password=ph.hash(password_sign_up)
        )
        with Session(engine) as session:
            session.add(user)
            session.commit()

    def check_username_exists(self, user_name: str) -> bool:
        """
        Checks if the username exists in the _secret_auth.json file.

        Args:
            user_name (str): username to check

        Return:
            bool: If username exists -> "True"; if not -> "False"
        """
        try:
            with Session(engine) as session:
                statement = select(User).where(User.username == user_name)
                user = session.exec(statement).one()
                if user:
                    return True
        except NoResultFound:
            return False
        return False

    def check_email_exists(self, email_forgot_passwd: str):
        """
        Checks if the email entered is present in the _secret_auth.json file.

        Args:
            email_forgot_passwd (str): email connected to forgotten password

        Return:
            Tuple[bool, Optional[str]]: If exists -> (True, <username>); If not, (False, None)
        """
        try:
            with Session(engine) as session:
                statement = select(User).where(User.email == email_forgot_passwd)
                user = session.exec(statement).one()
                if user:
                    return True, user.username
        except NoResultFound:
            return False, None
        return False, None

    def change_passwd(self, email_: str, random_password: str) -> None:
        """
        Replaces the old password with the newly generated password.

        Args:
            email_ (str): email connected to account
            random_password (str): password to set

        Return:
            None
        """
        with Session(engine) as session:
            statement = select(User).where(User.email == email_)
            user = session.exec(statement).one()
            if user:
                user.hashed_password = ph.hash(random_password)
                session.add(user)
                session.commit()
                

if __name__ == "__main__":
    create_db_and_tables(engine)
    create_user(engine)
    select_user(engine)