from sqlalchemy.orm import Session
from . import schemas, models


def create_production(
    session: Session,
    production: schemas.ProductionCreate,
):
    prod = models.Production(**production.model_dump())
    session.add(prod)
    session.commit()
    return prod


def list_production(session: Session):
    items = session.query(models.Production).all()
    return items
