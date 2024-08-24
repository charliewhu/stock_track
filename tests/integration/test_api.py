from datetime import datetime, date
from src.api import models


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


def test_list_production(client, session):
    data = [
        models.Production(date=datetime(2024, 1, 1), quantity=100),
        models.Production(date=datetime(2024, 1, 2), quantity=150),
        models.Production(date=datetime(2024, 1, 3), quantity=200),
    ]

    session.add_all(data)
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
