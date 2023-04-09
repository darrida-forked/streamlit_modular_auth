import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.sessions import SessionMiddleware

from src import webapps_login
from src.config import config

# from src.database.connection_pool import pool
from src.routers.auth import views as auth_views
from src.routers.maintenance import views as maint_views

app = FastAPI(title="FastAPI", description="FastAPI", version="0.0.0")

app.include_router(
    auth_views.router,
    prefix="",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    maint_views.router,
    prefix="/maint",
    tags=["Maintenance"],
    # dependencies=[Security(auth_views.get_current_active_user, scopes=["admin"])],
    responses={404: {"description": "Not found"}},
)


# Start/Stop Heroku Postgres Connection Pool
# @app.on_event("startup")
# def open_pool():
#     pool.open()


# @app.on_event("shutdown")
# def close_pool():
#     pool.close()


# Root endpoint to check for up status
class ServiceStatus(BaseModel):
    greeting: str = "I'm here!"


@app.get("/", response_model=ServiceStatus, tags=["Service Status"])
async def service_status():
    return ServiceStatus()


def main():
    https_only = True if config.SECURE_COOKIES is True else False
    app.add_middleware(SessionMiddleware, secret_key=config.STARLETTE_MIDDLEWARE_SECRET, https_only=https_only)
    webapps_login.init(app)
    uvicorn.run(app=app, port=8000)


if __name__ in {"__main__", "__mp_main__"}:
    main()
