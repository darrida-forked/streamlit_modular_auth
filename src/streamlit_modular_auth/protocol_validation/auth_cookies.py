import time

from rich import print
from streamlit_cookies_manager import CookieManager

from ..protocols import AuthCookies


def validate_auth_cookies(auth_cookies: AuthCookies, cookies: CookieManager):
    test_account = {"name": "test_name", "email": "test@email.com", "username": "user1", "password": "password1"}

    print("\n[bold white]VALIDATE `AuthCookies` PROTOCOL[/bold white]")

    # Check that auth cookies set and check successfully
    auth_cookies.set(test_account["username"], cookies)
    check = auth_cookies.check(cookies)
    if check:
        print("[bold magenta]set() and check()[/bold magenta]: [bold green]PASS[/bold green]")
    else:
        print("[bold magenta]set() and check()[/bold magenta]: [bold red]FAILED[/bold red]")

    # Check that cookies auto expire
    auth_cookies.set(test_account["username"], cookies, expire_delay=2)
    check = auth_cookies.check(cookies)
    if not check:
        print("[bold magenta]auto expire[/bold magenta]: " "[bold blue]INITIAL SET FAILED - UNABLE TO TEST[/bold blue]")
    else:
        time.sleep(3)
        check = auth_cookies.check(cookies)
        if not check:
            print("[bold magenta]auto expire[/bold magenta]: [bold green]PASS[/bold green]")
        else:
            print("[bold magenta]auto expire[/bold magenta]: [bold red]FAILED[/bold red]")

    # Check that cookies manually expire
    auth_cookies.set(test_account["username"], cookies, expire_delay=100)
    check = auth_cookies.check(cookies)
    if not check:
        print("[bold magenta]expire()[/bold magenta]: [bold blue]INITIAL SET FAILED - UNABLE TO TEST[/bold blue]")
    else:
        auth_cookies.expire(cookies)
        check = auth_cookies.check(cookies)
        if not check:
            print("[bold magenta]expire()[/bold magenta]: [bold green]PASS[/bold green]")
        else:
            print("[bold magenta]expire()[/bold magenta]: [bold red]FAILED[/bold red]")
