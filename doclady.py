from bs4 import BeautifulSoup
import re
from datetime import datetime
from settings import get_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from db.database import User, Presentation

irids = list()
creators_db = list()
preses = list()

file = open("all_doklady.xml", "r", encoding="utf-8")
xml_file = file.read()
soup = BeautifulSoup(xml_file, features="xml")
settings = get_settings()
engine = create_engine(str(settings.DB_DSN))
with Session(bind=engine) as session:
    for tag in soup.find_all("presentation"):
        preses.append(tag)
        for creator in tag.find_all("creator"):
            result = re.match(r"([а-яА-Яa-zA-Zё .]+)(\d+)", creator.text)
            if not (result is None):
                if result[2] not in irids:
                    irids.append(result[2])
                    user = User(name=result[1], irid=result[2])
                    creators_db.append(user)
                    session.add(user)
                    session.commit()
        presentation = Presentation(
            title=tag.title.text,
            conference=tag.conference.text,
            publicationDate=tag.publicationDate.text,
            start=datetime.strptime(tag.start.text, '%d.%m.%Y'),
            end=datetime.strptime(tag.end.text, '%d.%m.%Y'),
            place=tag.place.text if tag.place else None,
            kind=tag.kind.text,
            presentationid=tag.presentationid.text,
            confid=tag.confid.text,
            created=datetime.strptime(tag.created.text, '%Y-%m-%d %H:%M:%S')
        )
        session.add(presentation)
        session.commit()

        presentation.users = creators_db
        session.commit()
