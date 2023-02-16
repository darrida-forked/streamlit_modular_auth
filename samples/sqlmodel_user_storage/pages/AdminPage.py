# src.pages.Admin.py

import streamlit as st

# from src.apps.admin.models import User
from src.apps.admin.admin import AdminPage

page = AdminPage()


st.markdown("## Admin Tools")

st.markdown("---")

if not page.check_permissions():
    st.warning("Insufficient permissions.")
else:
    page.check_state()
    # LIST USERS
    user_tab, edit_tab, group_tab = st.tabs(["Users List", "User Changes", "Groups List"])
    with user_tab:
        if user := st.session_state["page"].get("open_user"):
            page.user_info(user)
        elif st.session_state["page"].get("create_user"):
            page.create_user()
        else:
            users = page.user_get_all()
            page.users_list(users)
            if st.button("Create User"):
                st.session_state["page"]["create_user"] = True
                st.experimental_rerun()

    # ADD GROUP
    with edit_tab:
        add_group = st.empty()
        with add_group.form("Add Group"):
            username = st.text_input("Username")
            groups = st.text_input("Group")
            st.markdown("###")
            add_group_button = st.form_submit_button(label="Add")

        if add_group_button is True:
            if result := page.user_add_groups(username, groups):
                st.success("Added group(s).")

        # REMOVE GROUP
        remove_group = st.empty()
        with remove_group.form("Remove Group"):
            username = st.text_input("Username")
            group = st.text_input("Delete Group")
            st.markdown("###")
            remove_group_button = st.form_submit_button(label="Remove")

        if remove_group_button is True:
            if result := page.user_delete_group(username, group):
                st.success("Removed group.")

    with group_tab:
        groups = page.group_get_all(return_str=False)
        # groups = [x.name for x in groups]
        page.groups_list(groups)
        if st.button("Add Group") or page.state["page"].get("add_group"):
            page.state["page"]["add_group"] = True
            name = st.text_input("Group Name")
            col1, col2, spacer = st.columns((0.5, 0.5, 2))
            with col1:
                if st.button("Create"):
                    if not name:
                        st.warning("Name required")
                    else:
                        if group := page.create_group(name):
                            st.success(f"Group {group} created.")
                        page.state["page"].pop("add_group")
                        st.experimental_rerun()
            with col2:
                if st.button("Close"):
                    page.state["page"].pop("add_group")
                    st.experimental_rerun()
