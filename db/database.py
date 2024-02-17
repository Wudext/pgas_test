from __future__ import annotations

import logging
from enum import Enum

from fastapi_sqlalchemy import db
from sqlalchemy import Enum as DbEnum
from sqlalchemy import ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

class Kind(str, Enum):
    ORAL: str = "oral"
    POSTER: str = "poster"


class Presentation(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    conference: Mapped[str] = mapped_column(String)
    publicationDate: Mapped[str] = mapped_column(String)
    start: Mapped[datetime] = mapped_column(DateTime)
    end: Mapped[datetime] = mapped_column(DateTime)
    place: Mapped[str] = mapped_column(String)
    kind: Mapped[Kind] = mapped_column(DbEnum(Kind, native_enum=False), nullable=False)
    presentationid: Mapped[int] = mapped_column(String, unique=True)
    confid: Mapped[int] = mapped_column(Integer, unique=True)
    created: Mapped[datetime] = mapped_column(DateTime)
