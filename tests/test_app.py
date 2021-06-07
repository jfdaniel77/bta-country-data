from chalice.test import Client
from app import app

def test_get_country_list():
    with Client(app) as client:
        response = client.http.get('/country')
        assert len(response.json_body) > 0
     
def test_get_currency():
    with Client(app) as client:
        response = client.http.get('/currency/Singapore')
        assert response.json_body[0] == {"currency": "Singapore Dollar"}
