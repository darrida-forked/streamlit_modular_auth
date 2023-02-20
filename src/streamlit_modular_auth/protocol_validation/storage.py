import random
import string
from rich import print
from ..protocols import UserAuth, UserStorage


def validate_user_storage(storage: UserStorage, auth: UserAuth):
    random_email = "".join(random.choices(string.ascii_lowercase, k=10)) + "@email.com"
    random_username = "".join(random.choices(string.ascii_lowercase, k=10))

    test_account = {
        "first_name": "fname",
        "last_name": "lname",
        "email": random_email,
        "username": random_username,
        "password": "password1",
    }

    print("\n[bold white]VALIDATE `UserStorage` PROTOCOL[/bold white]")

    # Register Account
    # - Then confirm account exists and auth works using UserAuth method
    storage.register(**test_account)
    if auth.check_credentials(test_account["username"], test_account["password"]):
        print("[bold magenta]register()[/bold magenta] account: " "[bold green]PASS[/bold green]")
    else:
        if auth.check_credentials(test_account["username"], "password2"):
            print(
                "[bold magenta]register()[/bold magenta] account: "
                "[bold blue]EXISTS[/bold blue] (likely previous test run)"
            )
        else:
            print("[bold magenta]register()[/bold magenta] account: [bold red]FAILED[/bold red]")

    # Check for username
    exists = storage.check_username_exists(test_account["username"])
    if exists is True:
        print(
            "[bold magenta]check_username_exists()[/bold magenta] find registered user: "
            "[bold green]PASS[/bold green]"
        )
    else:
        print(
            "[bold magenta]check_username_exists()[/bold magenta] find registered user: " "[bold red]FAILED[/bold red]"
        )

    exists = storage.check_username_exists("invalid_user")
    if exists is False:
        print(
            "[bold magenta]check_username_exists()[/bold magenta]` rejects unknown user: "
            "[bold green]PASS[/bold green]"
        )
    else:
        print(
            "[bold magenta]check_username_exists()[/bold magenta] rejects unknown user: " "[bold red]FAILED[/bold red]"
        )

    # Get username from email
    username = storage.get_username_from_email(test_account["email"])
    if username == test_account["username"]:
        print(
            "[bold magenta]get_username_from_email()[/bold magenta] find registered username: "
            "[bold green]PASS[/bold green]"
        )
    else:
        print(
            "[bold magenta]get_username_from_email()[/bold magenta] find registered username: "
            "[bold red]FAILED[/bold red]"
        )

    username = storage.get_username_from_email("invalid@email.com")
    if username is None:
        print(
            "[bold magenta]get_username_from_email()[/bold magenta] rejects unknown email: "
            "[bold green]PASS[/bold green]"
        )
    else:
        print(
            "[bold magenta]get_username_from_email()[/bold magenta] rejects unknown email: "
            "[bold red]FAILED[/bold red]"
        )

    # Change password
    # - Then confirm auth still works with UserAuth method
    test_account["password"] = "password2"
    storage.change_password(test_account["email"], test_account["password"])
    if auth.check_credentials(test_account["username"], test_account["password"]):
        print("[bold magenta]change_password()[/bold magenta]: [bold green]PASS[/bold green]")
    else:
        print("[bold magenta]change_password()[/bold magenta]: [bold red]FAILED[/bold red]")
