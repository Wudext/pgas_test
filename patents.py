from bs4 import BeautifulSoup
import re
from datetime import datetime
from settings import get_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from db.database import User, Patent

irids = list()
creators_db = list()
preses = list()

file = open("all_patent.xml", "r", encoding="utf-8")
xml_file = file.read()
soup = BeautifulSoup(xml_file, features="xml")
settings = get_settings()
engine = create_engine(str(settings.DB_DSN))
with Session(bind=engine) as session:
    for tag in soup.find_all("patent"):
        preses.append(tag)
        for creator in tag.find_all("creator"):
            creators_db = [user.irid for user in session.query(User).all()]
            if int(creator["irid"]) not in irids:
                irids.append(creator["irid"])
            if (int(creator["irid"])) not in creators_db:
                session.add(User(
                    irid=int(creator["irid"]),
                    name=creator.text
                ))
                session.commit()

        patent = Patent(
            title=tag.title.text,
            number=int(tag.number.text),
            date=datetime.strptime(tag.date.text, "%d.%m.%Y"),
            created=datetime.strptime(tag.created.text, "%Y-%m-%d %H:%M:%S"),
            creators=irids
        )
        session.add(patent)
        session.commit()
