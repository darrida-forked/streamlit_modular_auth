# Brief Notes

## Configuration
- Login Settings
- Protocol Plugins
- Layout

### Login Settings
- ...

### Protocol Plugins
- ...

### Layout
- "app" settings done in a dedicated configuration file (i.e., initialize and configura `ModularAuth()` in `config.py` (i.e., `app = ModularAuth()`))
  - The only places that should import the configuration object are `Home.py` and pages modules in the `pages` directory
- `Login()` should be used in `Home.py`, and it should take the initialized can configured `ModularAuth` object (`login = Login(app)`)
  - If only `Login()` is needed, and no further page authorization behavior, Login can be initialized by itself without the need to use ModularAuth (it gets used by default behind the scenes for that scenario - `login = Login()`)
- `pages` should intialize a view class and should take the initialized can configured `ModularAuth` object (`view = DefaultBaseView(app)`)
  - If no futher central methods are needed, import `DefaultBaseView` diretly into `page` module.
  - if additional app-wide methods are needed in a base view object, create a class that inherits from the default base (i.e., `class BaseView(DefaultBaseView)`), and still initialize that new base view in a `page` module (i.e., `view = BaseView(app)`)
  - This can be layered as much as needed. If app wide base view is needed it could be `class BaseView(DefaultBaseView)`, and if you want the main `view` object for a specific page to carry additional optoins, that could be inherited by a view object specific to the page (i.e., `class HomeView(BaseView)`), and the top level view class would still be initialized on the actual `page` module, using the initialized and configured `ModularAuth` object (i.e., `view = HomeView(app)`)
