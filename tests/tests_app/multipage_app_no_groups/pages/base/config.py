from streamlit_modular_auth import config, Login
from handlers._test_user_storage import UserAuthTest, UserStorageTest


config.auth = UserAuthTest()
config.user_storage = UserStorageTest()
config.expire_delay = 15

login_obj = Login()
