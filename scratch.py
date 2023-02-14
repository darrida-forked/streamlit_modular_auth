from streamlit_modular_auth import Login, DefaultPageModel, DefaultPageView, ModularAuth
from streamlit_modular_auth._handlers import DefaultUserAuth, DefaultAuthCookies, DefaultUserStorage


app = ModularAuth()
app.plugin_auth_cookies = DefaultAuthCookies()
app.plugin_user_auth = DefaultUserAuth()
app.plugin_user_storage = DefaultUserStorage()
app.login_expire = 7200
app.login_hide_account_management = True


login = Login(app)
view = DefaultPageView(app)
model = DefaultPageModel(app)
