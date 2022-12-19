
## Custom Authentication
- Empowers a developer to create their own authentication method that can be passed in when intializing the `__login__` class.
- The most straightforward way to use this is to pair it with setting `hide_account_management` as `True`
  - Example: a separate LDAP server will be used for authentication, and no local user storage is required (in this case, user accounts are managed elsewhere). This would utilize the login screen generated from this library, while disabling 'Create Account', 'Forgot Password?', and 'Reset Password'.

### How to use
- Create a class that inherits from `streamlit_login_auth_ui.utils.UserAuth`
- Add a `UserAuth.check_password` method. Only `self` is a required parameter.
  - `check_password` requires 2 concepts:
    - (1) It must use `self.username` and `self.password` to validate an account
    - (2) It must return `True` if account is validated, or `False` if validation fails.
  - Outside of those two requirements, it can be designed to interact with an authentication method in many different ways (additional parameters in constructor in `check_password` or constructor, additional methods, etc).
- Simple example located in tests for this library: `CustomAuth` in `/streamlit_login_auth_ui/tests/__test_app.py`
- Database example using SQLModel to authenticate using users stored in SQLite database: `StreamLitSQLModelAuth` in `/streamlit_login_auth_ui/samples/dbmodel_storage.py`
- Functional code example:
```python
import streamlit as st
from streamlit_login_auth_ui.widgets import __login__
from streamlit_login_auth_ui.utils import UserAuth

class SampleAuth(UserAuth):
    def __init__(self, login_name=None, username=None, password=None):
        super().__init__(login_name, username, password)
    
    def check_password(self):
        if self.username == "hardcoded_user" and self.password == "hardcoded_password":  # Insecure; **Example Only**
            return True
        return False

__login__obj = __login__(auth_token = "courier_auth_token", 
                         company_name = "Shims",
                         width = 200, height = 250, 
                         custom_authentication=SampleAuth())

LOGGED_IN = __login__obj.build_login_ui()

if LOGGED_IN == True:
    st.markown("Your Streamlit Application Begins here!")
```

## Custom User Storage
- Empowers a developer to create their own user storage method that can be passed in when intializing the `__login__` class.
- This likely will also be paired with a `custom_authentication` method as well. User storage handles creating, updating, and reading user account information; authentication handles validating a login attempt. They are separate to enable only authentication to be used if required.

### How to use
- Requirements:
  - Create a class that inherits from `streamlit_login_auth_ui.utils.UserStorage`
  - The class requires the following methods:
    - `register_new_usr`
    - `check_username_exists`
    - `check_email_exists`
    - `change_passwd`
  - Use docstrings found in these 4 methods in `UserStorage` in `streamlit_login_auth_ui.utils.UserStorage` to find argment and return/closure requirements.
    - Note: Don't miss the returned tuple for `check_email_exists`
  - Outside of these requirements, the class can be designed to interact with storage in many different ways (additional methods, etc).
- Simple example located tests for this library: `StreamlitTestUserStorage` in `/streamlit_login_auth_ui/tests/__test_user_storage.py`
- Database example using SQLModel to authenticate using users stored in SQLite database: `StreamLitSQLModelStorage` in `/streamlit_login_auth_ui/samples/dbmodel_storage.py`
- Code example using StreamlitSQLModelAuth and StreamlitSQLModelStorage:
```python
import streamlit as st
from streamlit_login_auth_ui.widgets import __login__
from streamlit_login_auth_ui.samples import UserAuthSQLModel, UserStorageSQLModel

__login__obj = __login__(auth_token = "courier_auth_token", 
                         company_name = "Shims",
                         width = 200, height = 250, 
                         custom_authentication=UserAuthSQLModel(),
                         custom_user_storage=UserStorageSQLModel())

LOGGED_IN = __login__obj.build_login_ui()

if LOGGED_IN == True:
    st.markown("Your Streamlit Application Begins here!")
```

## Custom Forgot Password Message Method
- Empowers a developer to create their method for sending temporary passwords that can be passed in when intializing the `__login__` class.

### How to use
- Requirements:
  - Create a class that inherits from `streamlit_login_auth_ui.utils.ForgotPasswordMessage`
  - The class requires the following methods:
    - `send`
  - Use docstrings found in this method in `ForgotPasswordMessage` in `streamlit_login_auth_ui.utils.ForgotPasswordMessage` to find argment and return/closure requirements.
    - **Note**: Additional arguments can be added to the end of the current list, but not in the middle (existing code uses position based arguments when calling the method)
  - Outside of these requirements, the class can be designed to interact with storage in many different ways (additional methods, etc).
- Simple example located in tests for this library: `ForgotPasswordCustomMsgTest` in `/streamlit_login_auth_ui/tests/__test_forgot_password.py`
```python
import streamlit as st
from streamlit_login_auth_ui.widgets import __login__
from from __test_forgot_password import ForgotPasswordCustomMsgTest

__login__obj = __login__(
    auth_token = "courier_auth_token", 
    company_name = "Shims",
    width = 200, height = 250, 
    custom_forgot_password = ForgotPasswordCustomMsgTest(
        message="Password via an insecure method"
    )
)

LOGGED_IN = __login__obj.build_login_ui()

if LOGGED_IN == True:
    st.markown("Your Streamlit Application Begins here!")
```