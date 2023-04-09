import json
import os
from collections import Counter
from pathlib import Path
from typing import Dict

# import diskcache

# dc = diskcache.Cache("cache")

session_info: Dict[str, Dict] = {}
counter = Counter()


shared_config_file = Path(__file__).resolve().parent.parent.parent / ".config.json"
with open(shared_config_file) as f:
    shared_config = json.load(f)


class config:
    # APP
    SECURE_COOKIES = os.environ.get("SECURE_COOKIES", False)
    # - The API_ENV environment variable needs to be set when running in production
    API_ENV = os.environ.get("API_ENV") or "heroku"
    API_USER_READ = os.environ.get("API_USER_READ") or "postgres"
    API_USER_WRITE = os.environ.get("API_USER_WRITE") or ""
    # - The following option is ONLY needed if testing using Windows WSL (Windows Subsystem for Linux)
    API_WSL = os.environ.get("API_WSL") or "false"
    API_TESTING = os.environ.get("API_TESTING") or "false"
    API_HTTPS = os.environ.get("API_HTTPS", False)

    # WEB HOST
    HOST = os.environ.get("API_HOST") or "0.0.0.0"  # noqa
    PORT = os.environ.get("API_PORT") or 8000
    WORKERS = os.environ.get("API_WORKERS") or 1
    LOG_LEVEL = os.environ.get("API_LOGL") or "debug"

    # CONNECTION POOL
    CONFIG_POOL_MIN_READ = 1
    CONFIG_POOL_MAX_READ = 3
    CONFIG_POOL_MIN_WRITE = 1
    CONFIG_POOL_MAX_WRITE = 3

    # DATABASE
    TEST_DB_FILE = Path(__file__).resolve().parent / "data" / "data-dev.sqlite"
    TEST_DB_STR = f"sqlite:///{TEST_DB_FILE}"
    PROD_DB_STR = os.environ.get("DATABASE_URL")

    POSTGRES_STR = shared_config["db_connect_str"]

    FASTAPI_SECRET_KEY = os.environ.get("FASTAPI_SECRET_KEY") or shared_config["fastapi_secret_key"]
    FASTAPI_ALGORITHM = os.environ.get("FASTAPI_ALGORITHM") or shared_config["fastapi_algorithm"]
    STARLETTE_MIDDLEWARE_SECRET = (
        os.environ.get("STARLETTE_MIDDLEWARE_SECRET") or shared_config["starlette_middleware_secret"]
    )
    STARLETTE_EXPIRE_AGE = os.environ.get("STARLETTE_MAX_AGE") or shared_config["starlette_expire_age"]
    WEBAPPS_LOGIN_REDIRECT = "http://localhost:8501"
