import streamlit as st

from .views import AdminView

view = AdminView()


def admin_page(view: AdminView):
    st.markdown("## Admin Tools")

    st.markdown("---")

    if not view.check_permissions():
        st.warning("Insufficient permissions.")
    else:
        view.check_state()
        # LIST USERS
        user_tab, edit_tab, group_tab = st.tabs(["Users List", "User Changes", "Groups List"])
        with user_tab:
            if user := st.session_state["page"].get("open_user"):
                view.user_info(user)
            elif st.session_state["page"].get("create_user"):
                view.create_user()
            else:
                users = view.user_get_all()
                view.users_list(users)
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
                if view.user_add_groups(username, groups):
                    st.success("Added group(s).")

            # REMOVE GROUP
            remove_group = st.empty()
            with remove_group.form("Remove Group"):
                username = st.text_input("Username")
                group = st.text_input("Delete Group")
                st.markdown("###")
                remove_group_button = st.form_submit_button(label="Remove")

            if remove_group_button is True:
                if view.user_delete_group(username, group):
                    st.success("Removed group.")

        with group_tab:
            groups = view.group_get_all(return_str=False)
            view.groups_list(groups)
            if st.button("Add Group") or view.state["page"].get("add_group"):
                view.state["page"]["add_group"] = True
                name = st.text_input("Group Name")
                col1, col2, spacer = st.columns((0.5, 0.5, 2))
                with col1:
                    if st.button("Create", key="groups_create"):
                        if not name:
                            st.warning("Name required")
                        else:
                            if group := view.create_group(name):
                                st.success(f"Group {group} created.")
                            view.state["page"].pop("add_group")
                            st.experimental_rerun()
                with col2:
                    if st.button("Close", key="groups_close"):
                        view.state["page"].pop("add_group")
                        st.experimental_rerun()
