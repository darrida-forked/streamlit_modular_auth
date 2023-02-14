from streamlit_modular_auth import Login, DefaultPageModel, DefaultPageView, ModularAuth
from streamlit_modular_auth._handlers import DefaultUserAuth, DefaultAuthCookies, DefaultUserStorage


app = ModularAuth()
app.config.custom_auth_cookies = DefaultAuthCookies()
app.config.custom_user_auth = DefaultUserAuth()
app.config.custom_user_storage = DefaultUserStorage()
app.config.expire_delay = 7200
app.config.hide_account_management = True

login = Login(app)
view = DefaultPageView(app)
model = DefaultPageModel(app)
