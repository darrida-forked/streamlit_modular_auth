from sqlalchemy import create_engine

from apps.admin.storage import SQLModelUserAuth, SQLModelUserStorage
from streamlit_modular_auth import ModularAuth

# requires psycopg2 or psycopg2-binary
db_url = "postgresql+psycopg2://postgres:easypass@localhost:5432/postgres"
pg_engine = create_engine(db_url)

app = ModularAuth(
    db_engine=pg_engine,
    plugin_user_storage=SQLModelUserStorage(),
    plugin_user_auth=SQLModelUserAuth(),
)
app.plugin_user_storage.db = app.db_engine
app.plugin_user_auth.db = app.db_engine
