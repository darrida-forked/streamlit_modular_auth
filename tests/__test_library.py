from typing import Union
from selenium.webdriver.chrome.options import Options

# ["--proxy-server='direct://'", "--proxy-bypass-list=*"]
# BROWSER OPTIONS
def Get_Proxy_Options(opts: list) -> Options:
    options = Options()
    for option in opts:
        options.add_argument(option)
    if options:
        return options
    return None
