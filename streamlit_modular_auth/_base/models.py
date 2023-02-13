from streamlit_modular_auth._base.config import Config, config


class DefaultPageModel:
    """Helper Methods for Backend Auth Logic

    Attributes:
    - state: Used in methods below; can be used for other purposes in an application using this auth library as well
    - cookies: Used in methods below; can be used for other purposes as well; "cookies" used for auth/session cookies
    """

    state = config.state
    cookies = config.cookies
    auth_cookies = config.auth_cookies

    def check_existing_session(self) -> bool:
        """Checks whether or not user is logged in

        Returns:
            bool: logged in status
        """
        if self.state.get("LOGGED_IN") is True:
            return True
        if self.auth_cookies.check(self.cookies) is True:
            self.state["LOGGED_IN"] = True
            return True
        return False

    def check_group_access(self, groups: list) -> bool:
        """Checks if user has access to required groups

        Args:
            groups (list): Permissions groups required for section/page (set in the class that inherits PageView)

        Returns:
            bool: page/section authorization status
        """
        if "groups" not in self.state.keys():
            user_groups = self.cookies.get("groups")
            if user_groups:
                self.state["groups"] = user_groups.split(",")
        else:
            user_groups = self.state["groups"]
        if not user_groups:
            return False
        groups.append("admin")
        return any(True for x in groups if x in user_groups)

    def setup(self, config: Config):
        self.state = config.state
        self.cookies = config.cookies
        self.auth_cookies = config.auth_cookies
