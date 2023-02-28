import streamlit as st
from sqlalchemy import create_engine

from streamlit_modular_auth import Login, ModularAuth

# requires psycopg2 or psycopg2-binary
db_url = "postgresql+psycopg2://postgres:easypass@localhost:5432/postgres"
pg_engine = create_engine(db_url)


app = ModularAuth()
app.db_engine = pg_engine
app.set_database_storage(use_admin=True)
login = Login(app)


st.markdown("## Streamlit Modular Auth")
st.markdown("### Default Postgres Configuration")

st.warning(
    "To initialize sqlite database: "
    "\n\n(1) run this app using the following format: "
    "`streamlit run <app>.py init_storage`"
    "\n\n(2) stop the app"
    "\n\n(3) start it again without `init_storage`"
)


if login.build_login_ui():
    st.success("You're logged in!")
else:
    st.info("You're not logged in yet...")
