from streamlit_modular_auth import protocols
from streamlit_modular_auth._apps.admin.page import AdminView, admin_page
from streamlit_modular_auth._core.config import ModularAuth, cookies
from streamlit_modular_auth._core.login import Login

# from streamlit_modular_auth._legacy.widgets import __login__  # noqa : F401
from streamlit_modular_auth._core.views import DefaultBaseView

__all__ = ["Login", "cookies", "ModularAuth", "config", "protocols", "DefaultBaseView", "AdminView", "admin_page"]
