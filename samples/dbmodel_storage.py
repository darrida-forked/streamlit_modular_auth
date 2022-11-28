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


sqlite_file_name = "sqlmodel_storage.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)#, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_user():
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


def select_user():
    try:
        with Session(engine) as session:
            statement = select(User).where(User.username == "user10")
            results = session.exec(statement).one()
            print(results)
        return True
    except NoResultFound:
        return False


class StreamLitSQLAlchemyAuth(StreamlitUserAuth):
    def __init__(self, login_name=None, username=None, password=None):
        super().__init__(login_name, username, password)
    
    def check_usr_pass(self):
        with Session(engine) as session:
            statement = select(User).where(User.username == self.username)
            user = session.exec(statement).one()
            if user:
                if ph.verify(user.hashed_password, self.password):
                    return True
        return False


class StreamLiteSQLAlchemyStorage(StreamlitUserStorage):
    storage_name: str = "sqlmodel"

    def check_unique_email(self, email_sign_up: str) -> bool:
        """
        Checks if the email already exists (since email needs to be unique).

        Args:
            email_sign_up (str): email for new account

        Return:
            bool: If email is unique -> "True"; if not -> "False"
        """
        try:
            with Session(engine) as session:
                statement = select(User).where(User.email == email_sign_up)
                email = session.exec(statement).one()
                if email:
                    return False
        except NoResultFound:
            return True
        return True

    def check_unique_usr(self, username_sign_up: str):
        """
        Checks if the username already exists (since username needs to be unique),
        also checks for non - empty username.

        Args:
            username_sign_up (str): username for new account

        Returns:
            bool: If username is unique -> "True"; if not -> "False"; if empty -> None
        """
        try:
            with Session(engine) as session:
                statement = select(User).where(User.username == username_sign_up)
                email = session.exec(statement).one()
                if email:
                    return False
        except NoResultFound:
            return True
        return True

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
        # except IntegrityError as e:
        #     if "UNIQUE" not in str(e):
        #         raise IntegrityError(e) from e
        #     print(f"User with username {user.username} and/or email {user.email} already exists.")

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

    def check_current_passwd(self, email_reset_passwd: str, current_passwd: str) -> bool:
        """
        Authenticates the password entered against the username when 
        resetting the password.

        Args:
            email_reset_passwd (str): email for account
            current_passwd (str): existing password for account
        
        Return:
            bool: If password is correct -> "True"; if not -> "False"
        """
        if not email_reset_passwd or not current_passwd:
            return False
        with Session(engine) as session:
            statement = select(User).where(User.email == email_reset_passwd)
            user = session.exec(statement).one()
            if user:
                try:
                    if ph.verify(user.hashed_password, current_passwd):
                        return True
                except:
                    pass
        return False
                


if __name__ == "__main__":
    create_db_and_tables()
    create_user()
    select_user()