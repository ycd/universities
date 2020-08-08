import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="module")
def base_client():
    client = TestClient(app)
    yield client


def test_home(base_client):
    "Clients"
    response = base_client.get("/")

    "Status Code"
    assert response.status_code == 200

    "Response"
    assert response.json() == {
        "Please go to docs.": "universitiesapi.herokuapp.com/docs"
    }


async def test_country_and_name(base_client):
    "Clients"
    response_one = base_client.get("/search?country=tur&name=saban")
    response_two = base_client.get("/search?country=turkey&name=middle")

    "Status Code"
    assert response_one.status_code == 200
    assert response_two.status_code == 200

    "Response"
    assert response_one.json() == [
        {
            "name": "Sabanci University",
            "alpha_two_code": "TR",
            "country": "Turkey",
            "web_pages": "http://www.sabanciuniv.edu.tr/http://www.sabanciuniv.edu/",
            "domains": "sabanciuniv.edu.trsabanciuniv.edu",
            "state_province": null,
        }
    ]
    assert response_two.json() == [
        {
            "name": "Middle East Technical University",
            "alpha_two_code": "TR",
            "country": "Turkey",
            "web_pages": "http://www.metu.edu.tr/",
            "domains": "metu.edu.tr",
            "state_province": null,
        }
    ]


def test_alpha_two_code_and_name(base_client):
    "Clients"
    response_one = base_client.get("/search?name=krako&alpha_two_code=pl")
    response_two = base_client.get("/search?name=harva&alpha_two_code=us")

    "Status Code"
    assert response_one.status_code == 200
    assert response_two.status_code == 200

    "Response"
    assert response_one.json() == [
        {
            "name": "Pedagogical University of Krakow",
            "alpha_two_code": "PL",
            "country": "Poland",
            "web_pages": "http://www.wsp.krakow.pl/",
            "domains": "wsp.krakow.pl",
            "state_province": null,
        }
    ]
    assert response_two.json() == [
        {
            "name": "Harvard University",
            "alpha_two_code": "US",
            "country": "United States",
            "web_pages": "http://www.harvard.edu/",
            "domains": "harvard.edu",
            "state_province": null,
        }
    ]


def test_country(base_client):
    "Clients"
    response_one = base_client.get("/search?country=United States")
    response_two = base_client.get("/search?country=russia")

    "Status Code"
    assert response_one.status_code == 200
    assert response_two.status_code == 200

    "Response"
    response_one_body = response_one.json()
    response_two_body = response_two.json()
    response_one_body[0]["country"] == "United States"
    response_two_body[0]["country"] == "Russian Federation"


def test_name(base_client):
    "Clients"
    response_one = base_client.get("/search?name=University of California")
    response_two = base_client.get("/search?name=Stanfo")

    "Status Code"
    assert response_one.status_code == 200
    assert response_two.status_code == 200

    "Response"
    response_one_body = response_one.json()
    response_two_body = response_two.json()
    response_one_body[0]["name"] == "University of California, Berkeley"
    response_two_body[0]["name"] == "Stanford University"


def test_alpha_two_code(base_client):
    "Clients"
    response_one = base_client.get("/search?alpha_two_code=fr")
    response_two = base_client.get("/search?alpha_two_code=de")
    response_three = base_client.get("/search?alpha_two_code=gr")
    response_four = base_client.get("/search?alpha_two_code=il")

    "Status Code"
    assert response_one.status_code == 200
    assert response_two.status_code == 200
    assert response_three.status_code == 200
    assert response_four.status_code == 200

    "Response"
    response_one_body = response_one.json()
    response_two_body = response_two.json()
    response_three_body = response_three.json()
    response_four_body = response_four.json()
    response_one_body[0]["alpha_two_code"] == "France"
    response_two_body[0]["alpha_two_code"] == "Deutschland"
    response_three_body[0]["alpha_two_code"] == "Greece"
    response_four_body[0]["alpha_two_code"] == "Isreal"
