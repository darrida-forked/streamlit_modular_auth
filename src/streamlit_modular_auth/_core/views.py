import time
from typing import List

import streamlit as st
from streamlit.components.v1 import html
from streamlit_cookies_manager import CookieManager

from .config import ModularAuth


class DefauleBaseView:
    title: str
    name: str
    groups: List[str] = None  # []

    def __init__(self, app: ModularAuth = None):
        if not app:
            app = ModularAuth()
        self.cookies: CookieManager = app.cookies
        self.state = app.state
        self.auth_cookies = app.plugin_auth_cookies

    def check_permissions(self) -> bool:
        """Checks if user is (1) logged in, and (2) has permission for the page/section in question

        Returns:
            bool: authorization status
        """
        if not self.check_existing_session():
            st.warning("Not logged in...")
            with st.spinner("Redirecting..."):
                time.sleep(1)
                self.change_page("")
        if hasattr(self, "groups"):
            return self.check_group_access(self.groups)
        else:
            return True

    def check_state(self):
        """Helper method that resets "page" value if a different page is loaded"""
        if self.state.get("page") and self.state["page"].get("name") == self.name:
            return
        if self.state.get("page"):
            self.state.pop("page")
        self.state["page"] = {"name": self.name}
        st.experimental_rerun()

    def change_page(self, page_name, timeout_secs=3):
        """Changes Streamlit pages in Multi-Page App
        - Found here: https://github.com/streamlit/streamlit/issues/4832#issuecomment-1201938174
        - Should be **REPLACED** when Streamlit releases native way to accomplish this

        Example usage (from issue post):
        ```
        if st.button("< Prev"):
            change_page("Foo")
        if st.button("Next >"):
            change_page("Bar")
        ```
        """
        nav_script = """
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {
                    if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
                        links[i].click();
                        return;
                    }
                }
                var elasped = new Date() - start_time;
                if (elasped < timeout_secs * 1000) {
                    setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
                } else {
                    alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
                }
            }
            window.addEventListener("load", function() {
                attempt_nav_page("%s", new Date(), %d);
            });
        </script>
        """ % (
            page_name,
            timeout_secs,
        )
        html(nav_script)

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
        if not groups:
            return True
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

    # def setup(self, config: Config):
    #     self.cookies = config.cookies
    #     self.state = config.state
