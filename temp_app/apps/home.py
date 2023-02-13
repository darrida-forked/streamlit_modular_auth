from pages.base.views import PageView
from pages.base.models import PageModel


class HomeView(PageView):
    title = "Home"
    name = "home"
    groups = []


class HomeModel(PageModel):
    ...
