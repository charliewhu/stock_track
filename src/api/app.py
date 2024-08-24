from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from . import schemas, services
from .dependencies import get_db

app = FastAPI()


@app.post("/", response_model=schemas.Production)
def create_production(
    production: schemas.ProductionCreate,
    session: Session = Depends(get_db),
):
    return services.create_production(session, production)


@app.get("/", response_model=list[schemas.Production])
def list_production(session: Session = Depends(get_db)):
    return services.list_production(session)
