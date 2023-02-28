from sqlalchemy import create_engine

from streamlit_modular_auth import ModularAuth

# requires psycopg2 or psycopg2-binary
db_url = "postgresql+psycopg2://postgres:easypass@localhost:5432/postgres"
pg_engine = create_engine(db_url)

app = ModularAuth(
    db_engine=pg_engine,
)
app.set_database_storage(use_admin=True)
