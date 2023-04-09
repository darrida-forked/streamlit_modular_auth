import json
import secrets

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from loguru import logger
from nicegui import ui

from src.config import config, session_info
from src.routers.auth import views as auth_views


def init(app: FastAPI) -> None:
    webapps = WebappsLogin()
    webapps.routes()
    ui.run_with(app)


class WebappsLogin:
    title = "Login"

    def routes(self):
        @ui.page("/login", dark=True)
        async def login(request: Request) -> None:
            ui.colors(primary="#6E93D6", secondary="#53B689", accent="#111B1E", positive="#53B689")
            with ui.header().classes("justify-between text-white pt"):
                ui.label("Entsy Webapps Login").classes("font-bold mt-2")

            logger.info(f"top: {request.session}")
            self._create_session_if_empty(request)
            if "authenticated" in session_info[request.session["id"]]:
                return RedirectResponse(config.WEBAPPS_LOGIN_REDIRECT)
            self._login_view(request)

        @ui.page("/logout")
        def logout(request: Request):
            if request.session["id"] in session_info:
                del session_info[request.session["id"]]
            if "id" in request.session:
                del request.session["id"]
            return RedirectResponse("/login")

    def _create_session_if_empty(self, request: Request):
        if "id" not in request.session or request.session["id"] not in session_info:
            logger.warning("Initializing new session")
            request.session["id"] = secrets.token_hex(48)
            session_info[request.session["id"]] = {}

    def _authenticate(self, username: str, password: str, request: Request):
        try:
            if auth_info := auth_views.login_for_access_token_func(
                username, password, config.STARLETTE_EXPIRE_AGE / 60
            ):
                session_info[request.session["id"]] = {
                    "access_token": auth_info["access_token"],
                    "authenticated": True,
                }
                logger.info(f"Session ID: {request.session}")
                logger.info(f'Access Token: {session_info[request.session["id"]]["access_token"]}')
                logger.info(f"session_info: {session_info}")
                logger.info("WRITE JSON")
                with open("/Users/ben/Documents/github/session_info.json", "w") as f:
                    json.dump(session_info, f)
                ui.open(config.WEBAPPS_LOGIN_REDIRECT)
                # ui.open("/home")
        except HTTPException:
            ui.notify("Invalid username or password", type="warning")

    def _login_view(self, request: Request):
        def authenticate():
            self._authenticate(username.value, password.value, request)

        with ui.row().classes("mx-auto content-center"):
            with ui.card().classes("absolute-center"):
                username = ui.input("Username").on("keydown.enter", authenticate)
                password = ui.input("Password", password=True, password_toggle_button=True).on(
                    "keydown.enter", authenticate
                )
                ui.button("Login", on_click=authenticate)
