from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, create_engine, Session, select
from sqlalchemy.exc import IntegrityError, NoResultFound
from streamlit_login_auth_ui.utils import ph, UserAuth


class UserAuthLDAP(UserAuth):
    def __init__(self, login_name=None, username=None, password=None, 
                 ldap_server: str = None, ldap_port: str = None, ldap_group: str = None):
        super().__init__(login_name, username, password)
    
    def check_password(self):
        """
        User `self.username` and `self.username` to verify credentials with LDAP server
        """
        ...