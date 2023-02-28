from apps.admin.page import admin_page
from apps.admin.views import AdminView
from config import app

view = AdminView(app)

admin_page(view)
