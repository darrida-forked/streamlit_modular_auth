import secrets
from typing import List

import streamlit as st
from argon2 import PasswordHasher
from sqlalchemy.exc import IntegrityError, NoResultFound

from streamlit_modular_auth._core.views import DefaultBaseView

from .db import db_pool  # engine
from .models import Group, User


class AdminView(DefaultBaseView):
    title = "Admin Tools"
    name = "admin"
    groups = ["admin"]
    db = db_pool

    # CALLABLES FOR INPUT WIDGETS
    def change_user_status(self, username, active):
        if active is True:
            self.user_disable(username)
        else:
            self.user_enable(username)

    def change_group_status(self, name, active):
        print(name, active)
        if active is True:
            print("Attempt to disable")
            self.group_disable(name)
        else:
            print("Attempt to enable")
            self.group_enable(name)

    def change_user_group_status(self, username: str, group: str, granted):
        if not granted:
            if not User.add_group(username, group):
                st.error("Found no record for user.")
            # self.user_add_groups(username, group)
        else:
            if not User.delete_group(username, group):
                st.error("Found no record for user.")
            # self.user_delete_group(username, group)

    def open_user_info(self, username):
        # with Session(self.db) as session:
        #     statement = select(User).where(User.username == username)
        #     if user := session.exec(statement).one():
        #         st.session_state["page"]["open_user"] = user
        user = User.get(username)
        st.session_state["page"]["open_user"] = user

    # FUNCTIONALITY
    def user_info(self, user: User = None):
        st.markdown("### User Info")

        if self.state["page"].get("user_info_updated"):
            st.info("User info updated.")
            self.state["page"].pop("user_info_updated")

        password = None
        # USER INFORMATION
        col1, _, col2, col3, _ = st.columns((0.4, 0.1, 0.05, 0.2, 0.25), gap="small")  # ["Information", "Groups"])
        with col1:
            user.username = st.text_input("Username", value=user.username or None)
            user.first_name = st.text_input("First Name", value=user.first_name or None)
            user.last_name = st.text_input("Last Name", value=user.last_name or None)
            user.email = st.text_input("Email", value=user.email or None)
            # auth_option = st.selectbox("Authentication", ("LDAP", "Password", "LDAP and Password"))
            # if auth_option in ("Password", "LDAP and Password"):
            password = st.text_input("Password", type="password", placeholder="*************")

            # user.ldap = auth_option in ("LDAP", "LDAP and Password")

        # USER PERMISSION GROUPS
        # all_groups = Group.get_all()
        all_groups = self.group_get_all()
        permissions = User.get_groups(user.username)
        # permissions = self.user_get_groups(user.username)
        for i, group in enumerate(all_groups, start=1):
            group_checkbox = col2.empty()
            col3.write(group)
            if group:
                granted = group in permissions
            group_checkbox.checkbox(
                label="",
                value=granted,
                key=f"{i}_group_list",
                on_change=self.change_user_group_status,
                args=[user.username, group, granted],
            )

        # RECORD DATES
        created_col, updated_col, _ = st.columns(3)
        with created_col:
            st.markdown(f"**Create Date:** {str(user.create_date)[:16] or ''}")
            st.markdown(f"**Create User:** {user.created_by or ''}")
        with updated_col:
            st.markdown(f"**Update Date:** {str(user.update_date)[:16] or ''}")
            st.markdown(f"**Update User:** {user.updated_by or ''}")

        # BUTTONS
        save_col, close_col, _ = st.columns((0.25, 0.25, 2))
        with save_col:
            if st.button("Save"):
                if password:
                    ph = PasswordHasher()
                    user.hashed_password = ph.hash(password)
                # self.user_update(user)
                User.update(user)
                self.state["page"]["user_info_updated"] = True
                st.experimental_rerun()
        with close_col:
            if st.button("Close"):
                st.session_state["page"].pop("open_user")
                st.experimental_rerun()

    def create_user(self):
        # CREATE USER
        create_user = st.empty()
        with create_user.form("Create User"):
            username = st.text_input("Username", placeholder="Xnumber or Username")
            first_name = st.text_input("First Name", placeholder="User's first name")
            last_name = st.text_input("Last Name", placeholder="User's last name")
            email = st.text_input("Email", placeholder="Unique email")
            # ldap = st.checkbox("Authenticate using LDAP", value=True)
            password = st.text_input("Password", type="password", value=secrets.token_urlsafe(45))
            st.markdown("###")
            create_user = st.form_submit_button(label="Create")

        if create_user is True:
            # storage = DefaultDBUserStorage()
            try:
                # storage.register(
                User.create(
                    first_name=first_name, last_name=last_name, email=email, username=username, password=password
                )
                # with Session(self.db) as session:
                #     statement = select(User).where(User.username == username)
                #     if session.exec(statement).one():
                #         st.success("User created.")
                if User.get(username):
                    st.success("User created.")
            except NoResultFound:
                st.error("An error occurred while attempting to create user.")
            except IntegrityError:
                st.warning("User or email address already exists.")
        if st.button("Close"):
            st.session_state["page"].pop("create_user")
            st.experimental_rerun()

    def users_list(self, users: List[User]):
        st.write("### User List")
        for i, user in enumerate(users, start=1):
            col1, col2, col3, col4, col5 = st.columns((0.5, 1, 1, 1, 1))
            active_checkbox = col1.empty()
            col2.write(user.username)
            col3.write(f"{user.first_name} {user.last_name}")
            col4.write("Active" if user.active else "Inactive")
            open_button = col5.empty()

            active_checkbox.checkbox(
                label="", value=user.active, key=i, on_change=self.change_user_status, args=[user.username, user.active]
            )
            open_button.button("Open", key=f"{i}_open_user", on_click=self.open_user_info, args=[user.username])

    def groups_list(self, groups: List[Group]):
        page_state = st.session_state["page"]

        st.write("### Group List")
        if page_state.get("show_all_groups") is not True:
            if st.button("Show Inactive"):
                page_state["show_all_groups"] = True
                st.experimental_rerun()
            groups = [x for x in groups if x.active is True]
        elif page_state["show_all_groups"] is True:
            if st.button("Hide Inactive"):
                page_state.pop("show_all_groups")
                st.experimental_rerun()
        for i, group in enumerate(groups, start=1):
            col1, col2, _, _, _ = st.columns((0.5, 1, 1, 1, 1))
            active_checkbox = col1.empty()
            col2.write(group.name)

            active_checkbox.checkbox(
                label="",
                value=group.active,
                key=f"{i}_groups",
                on_change=self.change_group_status,
                args=[group.name, group.active],
            )

    # def user_add_groups(self, username: str, groups: str) -> None:
    #     with Session(self.db) as session:
    #         group_statement = select(Group).where(Group.name == groups)
    #         group = session.exec(group_statement).one()
    #         user_statement = select(User).where(User.username == username)
    #         if user := session.exec(user_statement).one():
    #             user.groups.append(group)
    #             session.add(user)
    #             session.commit()
    #             return True
    #         else:
    #             import streamlit as st

    #             st.error("Found no record for user.")

    # def user_delete_group(self, username: str, group: str):
    #     with Session(self.db) as session:
    #         group_statement = select(Group).where(Group.name == group)
    #         group = session.exec(group_statement).one()
    #         user_statement = select(User).where(User.username == username)
    #         if user := session.exec(user_statement).one():
    #             if user.groups:
    #                 user.groups.remove(group)
    #                 session.add(user)
    #                 session.commit()
    #                 return True
    #         else:
    #             import streamlit as st

    #             st.error("Found no record for user.")

    # def user_get_groups(self, username: str):
    #     with Session(self.db) as session:
    #         statement = select(User).where(User.username == username)
    #         if user := session.exec(statement).one():
    #             return [x.name for x in user.groups] if user.groups else []
    #         else:
    #             st.error("Found no record for user.")

    def user_get_all(self):
        if users := User.get_all():
            return users
        st.error("Found no users.")

        # with Session(self.db) as session:
        #     statement = select(User)
        #     if users := session.exec(statement):
        #         return list(users)
        #     import streamlit as st

    # def user_update(self, user: User) -> None:
    #     """
    #     Saves the information of the new user in SQLModel database (SQLite)
    #     Args:
    #         name (str): name for new account
    #         email (str): email for new account
    #         username (str): username for new account
    #         password (str): password for new account
    #     Return:
    #         None
    #     """
    #     with Session(self.db) as session:
    #         statement = select(User).where(User.username == user.username)
    #         if saved_user := session.exec(statement).one():
    #             saved_user.active = user.active
    #             saved_user.email = user.email
    #             saved_user.last_name = user.last_name
    #             saved_user.hashed_password = user.hashed_password
    #             saved_user.active = user.active
    #             # saved_user.ldap = user.ldap
    #             saved_user.admin = user.admin
    #         session.add(saved_user)
    #         session.commit()

    def user_disable(self, username: str):
        User.set_status(False, username)
        # self._user_change_status(False, username)

    def user_enable(self, username: str):
        User.set_status(True, username)
        # self._user_change_status(True, username)

    @staticmethod
    def user_refresh_groups(self, username: str) -> None:
        if user := User.get(username):
            # with Session(self.db) as session:
            #     statement = select(User).where(User.username == username)
            #     if user := session.exec(statement).one():
            if user.groups:
                self.cookies.set("groups", user.groups)
                st.session_state["groups"] = user.groups.split(",")

    # def _user_change_status(self, change_to: bool, username: str):
    #     with Session(self.db) as session:
    #         statement = select(User).where(User.username == username)
    #         if user := session.exec(statement).one():
    #             user.active = change_to
    #             session.add(user)
    #             session.commit()
    #             return True
    #         else:
    #             import streamlit as st

    #             st.error("Found no record for user.")

    ##################################################################
    # GROUPS
    ##################################################################
    def create_group(self, name):
        return Group.create(name)
        # try:
        #     group = Group(name=name)
        #     with Session(self.db) as session:
        #         session.add(group)
        #         session.commit()
        # except IntegrityError as e:
        #     if "UNIQUE" not in str(e):
        #         raise IntegrityError(e) from e
        #     print(f"Group with name {group.name} already exists.")
        #     return False
        # return True

    def group_get_all(self, return_str=True) -> List["Group"]:
        groups = Group.get_all()
        if return_str and groups:
            return [x.name for x in groups]
        elif groups:
            return groups
        return None
        # groups_l = []
        # with Session(self.db) as session:
        #     statement = select(Group)
        #     groups = session.exec(statement)
        #     if return_str and groups:
        #         groups_l = [x.name for x in groups]
        #     elif groups:
        #         groups_l = list(groups)
        #     else:
        #         import streamlit as st

        #         st.error("Found no groups.")
        # return groups_l

    def group_disable(self, name: str):
        Group.set_status(False, name)
        # self._change_group_status(False, name)

    def group_enable(self, name: str):
        Group.set_status(True, name)
        # self._change_group_status(True, name)

    # def _change_group_status(self, change_to: bool, name: str):
    #     with Session(self.db) as session:
    #         statement = select(Group).where(Group.name == name)
    #         if group := session.exec(statement).one():
    #             group.active = change_to
    #             session.add(group)
    #             session.commit()
    #             return True
    #         else:
    #             import streamlit as st

    #             st.error("Found no record for group.")
