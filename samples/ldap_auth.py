from streamlit_modular_auth.protocols import UserAuth


class UserAuthLDAP(UserAuth):
    def __init__(self, ldap_server: str = None, ldap_port: str = None, ldap_group: str = None):
        self.ldap_server = ldap_server
        self.ldap_port = ldap_port
        self.ldap_group = ldap_group

    def check_password(self):
        """
        User `self.username` and `self.username` to verify credentials with LDAP server
        """
        ...
