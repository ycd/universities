from fastapi import FastAPI
from fastapi.responses import RedirectResponse, ORJSONResponse
from typing import List, Optional
from app.db.database import universities, database
from fastapi_utils.tasks import repeat_every
import requests
from asyncpg.exceptions import UniqueViolationError

tags_metadata = [
    {"name": "Search", "description": ""},
]


app = FastAPI(
    title="Universities API",
    openapi_tags=tags_metadata,
    default_response_class=ORJSONResponse,
)


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
    r = requests.get(
        "https://raw.githubusercontent.com/Hipo/university-domains-list/master/world_universities_and_domains.json"
    )
    data = r.json()

    for i in data:
        query = universities.insert().values(
            country=i["country"],
            name=i["name"],
            web_pages=i["web_pages"],
            alpha_two_code=i["alpha_two_code"],
            state_province=i["state-province"],
            domains=i["domains"],
        )

        try:
            await database.execute(query)
        except UniqueViolationError:
            pass


@app.get("/search", tags=["Search"])
async def search(
    country: Optional[str] = None,
    name: Optional[str] = None,
    alpha_two_code: Optional[str] = None,
    domain: Optional[str] = None,
):

    if country and name:
        query = (
            "SELECT * FROM universities WHERE country ILIKE '%"
            + country
            + "%' AND name ILIKE '%"
            + name
            + "%'"
        )
        return await database.fetch_all(query)

    elif alpha_two_code and name:
        query = (
            "SELECT * FROM universities WHERE alpha_two_code ILIKE '%"
            + alpha_two_code
            + "%' AND name ILIKE '%"
            + name
            + "%'"
        )
        return await database.fetch_all(query)

    elif country:
        query = "SELECT * FROM universities WHERE country ILIKE '%" + country + "%'"
        return await database.fetch_all(query)

    elif name:
        query = "SELECT * FROM universities WHERE name ILIKE '%" + name + "%'"
        return await database.fetch_all(query)

    elif alpha_two_code:
        query = (
            "SELECT * FROM universities WHERE alpha_two_code ILIKE '%"
            + alpha_two_code
            + "%'"
        )
        return await database.fetch_all(query)

    elif domain:
        query = "SELECT * FROM universities WHERE domains && '{" + domain + "}'"
        return await database.fetch_all(query)


@app.get("/", include_in_schema=False)
async def index():
    return RedirectResponse("/docs")
