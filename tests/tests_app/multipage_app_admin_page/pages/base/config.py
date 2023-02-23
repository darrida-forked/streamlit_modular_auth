from streamlit_modular_auth import ModularAuth

app = ModularAuth()
app.enable_admin_page()

# app.plugin_user_auth = UserAuthTest()
# app.plugin_user_storage = UserStorageTest()
# app.plugin_auth_cookies = UserAuthCookiesTest()
# app.login_expire = 15
