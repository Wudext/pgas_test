from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import Enum as DbEnum
from sqlalchemy import ForeignKey, Integer, String, DateTime, Boolean, Float, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import URLType

from .base import Base


class Kind(str, Enum):
    ORAL: str = "oral"
    POSTER: str = "poster"
    INVITED: str = "invited"
    PLENAR: str = "plenar"


class Presentation(Base):
    __tablename__ = "presentations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    conference: Mapped[str] = mapped_column(String)
    publicationDate: Mapped[str] = mapped_column(String)
    start: Mapped[datetime] = mapped_column(DateTime)
    end: Mapped[datetime] = mapped_column(DateTime)
    place: Mapped[str] = mapped_column(String, nullable=True)
    kind: Mapped[Kind] = mapped_column(DbEnum(Kind, native_enum=False), nullable=False)
    presentationid: Mapped[int] = mapped_column(String, unique=True)
    confid: Mapped[int] = mapped_column(Integer)
    created: Mapped[datetime] = mapped_column(DateTime)
    creators: Mapped[list[int]] = mapped_column(ARRAY(Integer))


class Patent(Base):
    __tablename__ = "patents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    number: Mapped[int] = mapped_column(Integer)
    date: Mapped[datetime] = mapped_column(DateTime)
    creators: Mapped[list[int]] = mapped_column(ARRAY(Integer))
    created: Mapped[datetime] = mapped_column(DateTime)


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    publicationName: Mapped[str] = mapped_column(String)
    issn: Mapped[str] = mapped_column(String, nullable=True)
    doi: Mapped[str] = mapped_column(String, nullable=True)
    journalRanking_value: Mapped[float] = mapped_column(Float, nullable=True)
    journalRanking_type: Mapped[str] = mapped_column(String, nullable=True)
    journalRanking_year: Mapped[str] = mapped_column(String, nullable=True)
    publisher: Mapped[str] = mapped_column(String)
    publicationDate: Mapped[str] = mapped_column(String)
    url: Mapped[str] = mapped_column(URLType)
    publicationID: Mapped[str] = mapped_column(String)
    is_vak: Mapped[bool] = mapped_column(Boolean)
    is_WoS: Mapped[bool] = mapped_column(Boolean)
    is_Scopus: Mapped[bool] = mapped_column(Boolean)
    is_RINC: Mapped[bool] = mapped_column(Boolean)

    val_WoS: Mapped[int] = mapped_column(Integer, nullable=True)
    val_Scopus: Mapped[int] = mapped_column(Integer, nullable=True)
    created: Mapped[datetime] = mapped_column(DateTime)
    attachments: Mapped[str] = mapped_column(String, nullable=True)

    users: Mapped[list[User]] = relationship(
        "User", secondary="articles_users", back_populates="articles"
    )


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    irid: Mapped[int] = mapped_column(Integer, unique=True)
    name: Mapped[str] = mapped_column(String)

# class PresUser(Base):
#     __tablename__ = "presentations_users"
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
#     project_id: Mapped[int] = mapped_column(Integer, ForeignKey("presentations.id"))
#
#
# class PatentUser(Base):
#     __tablename__ = "patents_users"
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
#     patent_id: Mapped[int] = mapped_column(Integer, ForeignKey("patents.id"))
