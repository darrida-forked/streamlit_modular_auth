from rich import print
from ..protocols import UserAuth, UserStorage


def validate_user_auth(auth: UserAuth, storage: UserStorage):
    test_account = {"name": "test_name", "email": "test2@email.com", "username": "user2", "password": "password1"}

    print("\n[bold white]VALIDATE `UserAuth` PROTOCOL[/bold white]")

    # Known User/Valid Password
    storage.register(**test_account)
    valid = auth.check_credentials(test_account["username"], test_account["password"])
    if valid:
        print(
            "[bold magenta]check_credentials()[/bold magenta] on known user/valid password: "
            "[bold green]PASS[/bold green]"
        )
    else:
        print(
            "[bold magenta]check_credentials()[/bold magenta] on known user/valid password: "
            "[bold red]FAILED[/bold red]"
        )

    # Known User/Invalid Password
    valid = auth.check_credentials(test_account["username"], "invalid_password")
    if not valid:
        print(
            "[bold magenta]check_credentials()[/bold magenta] on known user/INVALID password: "
            "[bold green]PASS[/bold green]"
        )
    else:
        print(
            "[bold magenta]check_credentials()[/bold magenta] on known user/INVALID password: "
            "[bold red]FAILED[/bold red]"
        )

    # Unknown User/"Valid" (for different account) Password
    valid = auth.check_credentials("unknown_user", test_account["password"])
    if not valid:
        print(
            "[bold magenta]check_credentials()[/bold magenta] Unknown user/valid password: "
            "[bold green]PASS[/bold green]"
        )
    else:
        print(
            "[bold magenta]check_credentials()[/bold magenta] Unknown user/valid password: "
            "[bold red]FAILED[/bold red]"
        )

    # Unknown User
    valid = auth.check_credentials("unknown_user", "invalid_password")
    if not valid:
        print("[bold magenta]check_credentials()[/bold magenta] Unknown user: [bold green]PASS[/bold green]")
    else:
        print("[bold magenta]check_credentials()[/bold magenta] Unknown user: [bold red]FAILED[/bold red]")
