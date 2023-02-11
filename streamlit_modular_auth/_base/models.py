from dataclasses import dataclass
from streamlit import session_state as st_session_state
from streamlit_modular_auth import cookies
from streamlit_modular_auth.protocols import AuthCookies


class PageModel:
    state: st_session_state = st_session_state
    cookies = cookies
    auth_cookies: AuthCookies

    def check_existing_session(self) -> bool:
        if self.state.get("LOGGED_IN") == True:
            return True
        if self.auth_cookies.check(self.cookies) == True:
            self.state["LOGGED_IN"] = True
            return True
        return False
    
    def check_group_access(self, groups: list) -> bool:
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
