from pages.base.config import app
from streamlit_modular_auth import AdminView, admin_page

view = AdminView(app)

admin_page(view)
