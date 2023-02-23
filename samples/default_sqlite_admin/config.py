from streamlit_modular_auth import ModularAuth


app = ModularAuth()
app.enable_admin_page()
app.set_sqlite_storage()
