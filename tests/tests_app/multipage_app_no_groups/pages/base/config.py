from streamlit_modular_auth import Login, ModularAuth
from handlers._test_user_storage import UserAuthTest, UserStorageTest


app = ModularAuth()
app.plugin_user_auth = UserAuthTest()
app.plugin_user_storage = UserStorageTest()
app.login_expire = 15

login = Login(app)
