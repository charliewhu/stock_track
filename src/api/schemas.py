import datetime
from pydantic import BaseModel, ConfigDict


class ProductionBase(BaseModel):
    date: datetime.date
    quantity: int


class ProductionCreate(ProductionBase):
    pass


class Production(ProductionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
