from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    pass


class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str] = mapped_column()
