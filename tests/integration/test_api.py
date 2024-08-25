from datetime import datetime, date

import pytest
from api import models


@pytest.fixture
def api_data():
    return [
        models.Production(date=datetime(2024, 1, 1), quantity=100),
        models.Production(date=datetime(2024, 1, 2), quantity=150),
        models.Production(date=datetime(2024, 1, 3), quantity=200),
    ]


def test_create_monthly_production(client, session):
    # post data to API
    # expect response of data + id
    # expect db to contain data
    data = {
        "date": f"{date.today()}",
        "quantity": 1000,
    }

    response = client.post(
        "/",
        json=data,
    )

    ids = [item.id for item in session.query(models.Production).all()]

    assert response.json() == {"id": 1, **data}
    assert response.json()["id"] in ids


def test_update_monthly_production(client, session, api_data):
    # create item in db
    session.add(api_data[0])
    session.commit()

    db_item: models.Production = session.query(models.Production).first()

    new_data = {
        "id": db_item.id,
        "date": date.today().isoformat(),
        "quantity": 9000,
    }

    # send put request to API
    response = client.put(
        f"/{db_item.id}",
        json=new_data,
    )

    # expect response to have correct data
    assert response.status_code == 200
    assert new_data["date"] == response.json()["date"]
    assert new_data["quantity"] == response.json()["quantity"]

    # assert db item matches new information
    db_item = session.query(models.Production).first()
    assert db_item.quantity == new_data["quantity"]
    assert db_item.date.isoformat() == new_data["date"]


def test_list_production(client, session, api_data):
    session.add_all(api_data)
    session.commit()

    response = client.get(
        "/",
    )

    for item in response.json():
        assert isinstance(item, dict)
        assert "id" in item
        assert "date" in item
        assert "quantity" in item

    assert len(response.json()) == 3
    assert sum([i["quantity"] for i in response.json()]) == 450
