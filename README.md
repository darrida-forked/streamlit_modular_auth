# Don't Use Yet - This Fork is under active development

## Configuration
- Login Settings
- Protocol Plugins
- Layout

## Login Settings
- ...

## Protocol Plugins
- ...

## Layout
- "app" settings done in a dedicated configuration file (i.e., initialize and configura `ModularAuth()` in `config.py` (i.e., `app = ModularAuth()`))
  - The only places that should import the configuration object are `Home.py` and pages modules in the `pages` directory
- `Login()` should be used in `Home.py`, and it should take the initialized can configured `ModularAuth` object (`login = Login(app)`)
  - If only `Login()` is needed, and no further page authorization behavior, Login can be initialized by itself without the need to use ModularAuth (it gets used by default behind the scenes for that scenario - `login = Login()`)
- `pages` should intialize a view class and should take the initialized can configured `ModularAuth` object (`view = DefaultBaseView(app)`)
  - If no futher central methods are needed, import `DefaultBaseView` diretly into `page` module.
  - if additional app-wide methods are needed in a base view object, create a class that inherits from the default base (i.e., `class BaseView(DefaultBaseView)`), and still initialize that new base view in a `page` module (i.e., `view = BaseView(app)`)
  - This can be layered as much as needed. If app wide base view is needed it could be `class BaseView(DefaultBaseView)`, and if you want the main `view` object for a specific page to carry additional optoins, that could be inherited by a view object specific to the page (i.e., `class HomeView(BaseView)`), and the top level view class would still be initialized on the actual `page` module, using the initialized and configured `ModularAuth` object (i.e., `view = HomeView(app)`)

## Examples

### **One Page Script with Default Handlers**
- Storage: local json file
- Auth: local one-way hashing and local authentication
- Additional Requirements: None

```python
import streamlit as st

from streamlit_modular_auth import Login

login = Login()


st.markdown("## Streamlit Modular Auth")
st.markdown("### Default Configuration")


if login.build_login_ui():
    st.success("You're logged in!")
```

### **One Page Script with SQLite Handlers**
- Storage: SQLite database file
- Auth: local one-way hasing amd local authentication
- Additional Requirements: One-time/first-time launch of the app with `init_storage` at the end of the CLI statement (i.e., `streamlit run your_module.py init_storage`). After database file is initialized, shut down the app, then start again without `init_storage`

```python
import streamlit as st

from streamlit_modular_auth import Login, ModularAuth

app = ModularAuth()
app.set_database_storage(hide_admin=True)
login = Login(app)


st.markdown("## Streamlit Modular Auth")
st.markdown("### Default SQLite Configuration")


if login.build_login_ui():
    st.success("You're logged in!")
```

### **One Page Script with Account Management Disabled**
- Storage: Example assumes custom handlers created (`MyUserAuth` and `MyUserStorage`)
- Auth: Example uses default one-way hashing and local authentication
- Additional Requirements:
  - This requires that you've created a method to create and manage accounts yourself (using streamlit-modular-auth supported protocols)
  - Protocols you'll need to create handlers based on: `streamlit_modular_auth.UserAuth`, `streamlit_modular_auth.UserStorage`
  - An example would be creating a user storage handler for Postgres, and setting up the user auth handler to validate authentation credentials against how those accounts are setup

```python
import streamlit as st
from my_handlers.user_storage import MyUserAuth, MyUserStorage

from streamlit_modular_auth import Login, ModularAuth

app = ModularAuth()
app.plugin_user_auth = MyUserAuth()
app.plugin_user_storage = MyUserStorage()
app.login_label = "My Login"
login = Login(app)


if login.build_login_ui():
    st.success("You're logged in!")
```

### **Mutipage App Script with Default SQLite Storage**
- Storage: Default SQLite storage
- Auth: Default one-way hashing and local authentication
- Additional Requirements:
  - Recommended app structure shown in comment at top of each file/block snippet

```python
# config.py

from streamlit_modular_auth import ModularAuth

app = ModularAuth()
app.set_database_storage(hide_admin=True)
```

```python
# Home.py

import streamlit as st
from config import app
from streamlit_modular_auth import Login

login = Login(app)

if login.build_login_ui():
    st.success("You're logged in!")
```

```python
# apps/pictures/views.py

from streamlit_modular_auth import DefaultBaseView


class PicturesView(DefaultBaseView):
    title = "Pictures"
```

```python
# pages/Second_Page.py

import streamlit as st
from apps.pictures.views import PicturesView
from config import app

view = PicturesView(app)

st.title(view.title)

if not view.check_permissions():
    pass
else:
    st.write("You're page starts here.")
```

### **Multipage App with Optional Admin Page**

```python
# config.py

from streamlit_modular_auth import ModularAuth

app = ModularAuth()
app.set_database_storage()
```

```python
# Home.py

import streamlit as st
from config import app
from streamlit_modular_auth import Login

login = Login(app)

if login.build_login_ui():
    st.success("You're logged in!")
```

```python
# apps/pictures/views.py

from streamlit_modular_auth import DefaultBaseView

class PicturesView(DefaultBaseView):
    title = "Pictures"
```

```python
# pages/Second_Page.py

import streamlit as st
from apps.pictures.views import PicturesView
from config import app

view = PicturesView(app)

st.title(view.title)

if not view.check_permissions():
    pass
else:
    st.write("You're page starts here.")
```

### **Supplimental**

#### App-Wide View Methods
- Instead of creating view classes for a specific page that inherity directly from `streamlit_auth_modular.BaseModelView`, create a central base view that inherits from `BaseModelView`, then have specific pages inherity that central base view.

```python
# base/base_view.py

from streamlit_modular_auth import DefaultBaseView

class AppBaseView(DefaultBaseView):
    
    def app_wide_method1():
        ...
    
    def app_wide_method2():
        ...
```

```python
# Page 1: apps/pictures/views.py

from base.base_view.py import AppBaseView

class PicturesView(AppBaseView):
    title = "Pictures"
```

```python
# Page 2: apps/poems/views.py

from base.base_view.py import AppBaseView

class PoemsView(AppBaseView):
    title = "Poems"
```