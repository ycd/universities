import sqlalchemy
from sqlalchemy import create_engine
import databases


## Postgres Database
DATABASE_URL = "postgresql://user:password@localhost:5432/universities"
# DATABASE_URL = os.environ.get("TRAVIS")
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


# SQLAlchemy database model
universities = sqlalchemy.Table(
    "universities",
    metadata,
    sqlalchemy.Column("name", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("alpha_two_code", sqlalchemy.String),
    sqlalchemy.Column("country", sqlalchemy.String),
    sqlalchemy.Column("web_pages", sqlalchemy.ARRAY(sqlalchemy.String)),
    sqlalchemy.Column("domains", sqlalchemy.ARRAY(sqlalchemy.String)),
    sqlalchemy.Column("state_province", sqlalchemy.String),
)

engine = sqlalchemy.create_engine(DATABASE_URL)

metadata.create_all(engine)
