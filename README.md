
HOW TO INSTALL ALL LIBRARIES:
python3.10 -m venv venv
source venv/bin/activate
python3.10 -m pip install -r requirement.txt

# Streamlit Login/ Sign Up Library   [![Downloads](https://static.pepy.tech/personalized-badge/streamlit-login-auth-ui?period=month&units=international_system&left_color=grey&right_color=blue&left_text=downloads)](https://pepy.tech/project/streamlit-login-auth-ui)

The streamlit_login_auth_ui library is meant for streamlit application developers.
It lets you connect your streamlit application to a pre-built and secure Login/ Sign-Up page.

You can customize specific parts of the page without any hassle!

The library grants users an option to reset their password, users can click on ```Forgot Password?``` after which an Email is triggered containing a temporary, randomly generated password.

The library also sets encrypted cookies to remember and automatically authenticate the users without password. \
The users can logout using the ```Logout``` button.


## Authors
- [@gauriprabhakar](https://github.com/GauriSP10)

## PyPi
https://pypi.org/project/streamlit-login-auth-ui/

## The UI:
![login_streamlit](https://user-images.githubusercontent.com/75731631/185765909-a70dd7af-240d-4a90-9140-45d6292e76f0.png)
 
## Installation

```python
pip install streamlit-login-auth-ui
```

## How to implement the library?

To import the library, just paste this at the starting of the code:
```python
from streamlit_login_auth_ui.widgets import __login__
```

All you need to do is create an object for the ```__login__``` class and pass the following parameters:
1. auth_token : The unique authorization token received from - https://www.courier.com/email-api/
2. company_name : This is the name of the person/ organization which will send the password reset email.
3. width : Width of the animation on the login page.
4. height : Height of the animation on the login page.
5. logout_button_name : The logout button name.
6. hide_menu_bool : Pass True if the streamlit menu should be hidden.
7. hide_footer_bool : Pass True if the 'made with streamlit' footer should be hidden.
8. lottie_url : The lottie animation you would like to use on the login page. Explore animations at - https://lottiefiles.com/featured
9. hide_registration : Pass True if 'Create Account' option should be hidden from Navigation.
10. hide_account_management : Pass True if all options other than 'Login' should be hidden from Navigation.
11. custom_authentication : Option to pass custom authentication class that inherits from StreamlitUserAuth (see information further below).
12. custom_user_storage : Option to pass custom user storage class that inherits from StreamLitUserStorage (see information further below).

#### Mandatory Arguments:
* ```auth_token```
* ```company_name```
* ```width```
* ```height```

#### Non Mandatory Arguments:
* ```logout_button_name```      [default = 'Logout']
* ```hide_menu_bool```          [default = False]
* ```hide_footer_bool```        [default = False]
* ```lottie_url```              [default = https://assets8.lottiefiles.com/packages/lf20_ktwnwv5m.json]
* ```hide_registration```       [default = False]
* ```hide_account_management``` [default = False]
* ```custom_authentication```   [default = None]
* ```custom_user_storage```     [default = None]

After doing that, just call the ```build_login_ui()``` function using the object you just created and store the return value in a variable.

# Example:
```python
import streamlit as st
from streamlit_login_auth_ui.widgets import __login__

__login__obj = __login__(auth_token = "courier_auth_token", 
                    company_name = "Shims",
                    width = 200, height = 250, 
                    logout_button_name = 'Logout', hide_menu_bool = False, 
                    hide_footer_bool = False, 
                    lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

LOGGED_IN = __login__obj.build_login_ui()

if LOGGED_IN == True:
    st.markown("Your Streamlit Application Begins here!")
```

That's it! The library handles the rest. \
Just make sure you call/ build your application indented under ```if st.session_state['LOGGED_IN'] == True:```, this guarantees that your application runs only after the user is securely logged in. 

## Explanation
### Login page
The login page, by default, authenticates the user using the ```_secret_auth_.json``` file.

### Create Account page
By default, this stores the user info in a secure way using the  ```_secret_auth_.json``` file. \
![create_account_streamlit](https://user-images.githubusercontent.com/75731631/185765826-3bb5d2ca-c549-46ff-bf14-2cc42d295588.png)

### Forgot Password page
After user authentication (email), triggers an email to the user containing a random password. \
![forgot_password_streamlit](https://user-images.githubusercontent.com/75731631/185765851-18db4775-b1f0-4cfe-86a7-93bda88227dd.png)

### Reset Password page
After user authentication (email and the password shared over email), resets the password and updates the same \
in the ```_secret_auth_.json``` file. \
![reset_password_streamlit](https://user-images.githubusercontent.com/75731631/185765859-a0cf45b0-bfa4-489d-8060-001a9372843a.png)

### Logout button
Generated in the sidebar only if the user is logged in, allows users to logout. \
![logout_streamlit](https://user-images.githubusercontent.com/75731631/185765879-dbe17dda-93e3-4417-b5fc-5ce1d4dc8ecc.png)

__Cookies are automatically created and destroyed depending on the user authentication status.__

## Custom Authentication
- Empowers a developer to create their own authentication method that can be passed in when intializing the `__login__` class.
- The most straightforward way to use this is to pair it with setting `hide_account_management` as `True`
  - Example: a separate LDAP server will be used for authentication, and no local user storage is required (in this case, user accounts are managed elsewhere). This would utilize the login screen generated from this library, while disabling 'Create Account', 'Forgot Password?', and 'Reset Password'.

### How to use
- Create a class that inherits from `streamlit_login_auth_ui.utils.StreamlitUserAuth`
- Add a `StreamlitUserAuth.check_password` method. Only `self` is a required parameter.
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
from streamlit_login_auth_ui.utils import StreamlitUserAuth

class SampleAuth(StreamlitUserAuth):
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
  - Create a class that inherits from `streamlit_login_auth_ui.utils.StreamlitUserStorage`
  - The class requires the following methods:
    - `register_new_usr`
    - `check_username_exists`
    - `check_email_exists`
    - `change_passwd`
  - Use docstrings found in these 4 methods in `StreamlitUserStorage` in `streamlit_login_auth_ui.utils.StreamlitUserStorage` to find argment and return/closure requirements.
    - Note: Don't miss the returned tuple for `check_email_exists`
  - Outside of these requirements, the class can be designed to interact with storage in many different ways (additional methods, etc).
- Simple example located tests for this library: `StreamlitTestUserStorage` in `/streamlit_login_auth_ui/tests/__test_user_storage.py`
- Database example using SQLModel to authenticate using users stored in SQLite database: `StreamLitSQLModelStorage` in `/streamlit_login_auth_ui/samples/dbmodel_storage.py`
- Code example using StreamlitSQLModelAuth and StreamlitSQLModelStorage:
```python
import streamlit as st
from streamlit_login_auth_ui.widgets import __login__
from streamlit_login_auth_ui.samples import StreamlitSQLModelAuth, StreamlitSQLModelStorage

__login__obj = __login__(auth_token = "courier_auth_token", 
                         company_name = "Shims",
                         width = 200, height = 250, 
                         custom_authentication=StreamlitSQLModelAuth(),
                         custom_user_storage=StreamlitSQLModelStorage())

LOGGED_IN = __login__obj.build_login_ui()

if LOGGED_IN == True:
    st.markown("Your Streamlit Application Begins here!")
```

## Development
- Create virtual environment
- Install dependencies from `requirements.txt`
- Install dependencies from `test-requirements.txt`
- Setup `geckodriver` for OS to be tested on
  - i.e., for MacOS Apple Silicon:
    ```
    export PATH=$PATH:$PWD/tests/utils/geckodriver_macos_arm64/.
    ```
- Change directory into tests, then execute `robotframework`
  ```
  cd tests
  robot .
  ```

## Version
v0.2.1

## License
[MIT](https://github.com/GauriSP10/streamlit_login_auth_ui/blob/main/LICENSE)






