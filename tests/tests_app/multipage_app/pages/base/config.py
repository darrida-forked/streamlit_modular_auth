from handlers._test_cookies import UserAuthCookiesTest
from handlers._test_user_storage import UserAuthTest, UserStorageTest

from streamlit_modular_auth import ModularAuth

app = ModularAuth(
    plugin_user_auth=UserAuthTest(),
    plugin_user_storage=UserStorageTest(),
    plugin_auth_cookies=UserAuthCookiesTest(),
    login_expire=15,
)
