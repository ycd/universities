import sqlalchemy
from sqlalchemy import and_, literal
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import insert
import databases
import psycopg2
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from typing import List, Optional
import requests
from asyncpg.exceptions import UniqueViolationError
import os


## Postgres Database
# DATABASE_URL = "postgresql://user:password@host:5432/universities"
DATABASE_URL = os.environ.get("TRAVIS")
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


tags_metadata = [
        {
            "name": "Search",
            "description": ""
        },

]


#SQLAlchemy database model
universities = sqlalchemy.Table(
	"universities",
	metadata,
	sqlalchemy.Column("name"          , sqlalchemy.String, primary_key=True),
	sqlalchemy.Column("alpha_two_code", sqlalchemy.String),
	sqlalchemy.Column("country"       , sqlalchemy.String),
	sqlalchemy.Column("web_pages"     , sqlalchemy.ARRAY(sqlalchemy.String)),
        sqlalchemy.Column("domains"       , sqlalchemy.ARRAY(sqlalchemy.String)),
        sqlalchemy.Column("state_province", sqlalchemy.String),
)

engine = sqlalchemy.create_engine(
	DATABASE_URL
)

metadata.create_all(engine)


# FastAPI
app = FastAPI(
	title="Universities API",
	openapi_tags=tags_metadata,
)



# **Database Connection**
@app.on_event("startup")
async def startup():
	await database.connect()


@app.on_event("shutdown")
async def shutdown():
	await database.disconnect()


@repeat_every(seconds=86400)
@app.on_event("startup")
async def update_database():
    """
    Asynchronous database updater, runs itself in 86400 seconds | 1 day
    """
    r = requests.get("https://raw.githubusercontent.com/Hipo/university-domains-list/master/world_universities_and_domains.json")
    data = r.json()

    for i in data:
        query = universities.insert().values(
		country = i["country"],
        name = i["name"],
        web_pages = i["web_pages"],
        alpha_two_code = i["alpha_two_code"],
        state_province = i["state-province"],
        domains = i["domains"],
        )

        try:
            await database.execute(query)
        except UniqueViolationError:
            pass

@app.get("/search", tags=["Search"])
async def search(country: Optional[str] = None, name: Optional[str] = None, alpha_two_code: Optional[str] = None, domain: Optional[str] = None) :

    if country and name:
        query = "SELECT * FROM universities WHERE country ILIKE '%"+country+"%' AND name ILIKE '%"+name+"%'"
        return await database.fetch_all(query)

    elif alpha_two_code and name:
        query = "SELECT * FROM universities WHERE alpha_two_code ILIKE '%"+alpha_two_code+"%' AND name ILIKE '%"+name+"%'"
        return await database.fetch_all(query)

    elif country:
        query = "SELECT * FROM universities WHERE country ILIKE '%"+country+"%'"
        return await database.fetch_all(query)

    elif name:
        query = "SELECT * FROM universities WHERE name ILIKE '%"+name+"%'"
        return await database.fetch_all(query)

    elif alpha_two_code:
        query = "SELECT * FROM universities WHERE alpha_two_code ILIKE '%"+alpha_two_code+"%'"
        return await database.fetch_all(query)

    elif domain:
        query = "SELECT * FROM universities WHERE domains && '{"+domain+"}'"
        return await database.fetch_all(query)


@app.get("/")
async def index():
    return {"Please go to docs.": "universitiesapi.herokuapp.com/docs"}
