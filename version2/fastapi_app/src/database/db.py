from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import config

# from fastapi.routers.auth.models import Base


class Base(DeclarativeBase):
    pass


engine = create_engine(config.TEST_DB_STR, pool_recycle=3600, echo=True)

if __name__ == "__main__":
    Base.metadata.create_all(engine)
