from pages.base.models import PageModel
from pages.base.views import PageView


class HomeView(PageView):
    title = "Home"
    name = "home"
    groups = []


class HomeModel(PageModel):
    ...
