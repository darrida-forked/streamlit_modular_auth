from pages.base.views import PageView
from pages.base.models import PageModel


class Page1View(PageView):
    title = "Page 1"
    name = "page"
    groups = ["page"]


class Page1Model(PageModel):
    ...
