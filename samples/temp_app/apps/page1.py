from pages.base.models import PageModel
from pages.base.views import PageView


class Page1View(PageView):
    title = "Page 1"
    name = "page"
    groups = ["page"]


class Page1Model(PageModel):
    ...
