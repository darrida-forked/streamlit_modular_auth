from typing import Protocol


class UserAuth(Protocol):
    login_name: str = "Login"
    username: str
    password: str

    def check_password(self) -> bool:
        ...


class UserStorage(Protocol):
    storage_name: str

    def register_new_user(self, name: str, email: str, username: str, password: str) -> None:
        ...

    def check_username_exists(self, username: str) -> bool:
        ...

    def check_email_exists(self, email: str):
        ...

    def change_passwd(self, email: str, password: str) -> None:
        ...


class ForgotPasswordMessage(Protocol):
    method_name: str

    def send_password(
        self, auth_token: str, username: str, email: str, company_name: str, reset_password: str
    ) -> None:
        ...


