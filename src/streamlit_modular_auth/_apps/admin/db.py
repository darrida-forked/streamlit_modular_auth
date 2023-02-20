from sqlmodel import create_engine


def initialize_db_engine():
    sqlite_file_name = "sqlmodel_storage.sqlite"
    sqlite_url = f"sqlite:///{sqlite_file_name}"
    return create_engine(sqlite_url)  # , echo=True)


engine = initialize_db_engine()
