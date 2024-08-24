import datetime
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Production(Base):
    __tablename__ = "production"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime.date] = mapped_column(unique=True, index=True)
    quantity: Mapped[int] = mapped_column()
