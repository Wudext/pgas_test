from bs4 import BeautifulSoup
import re
from datetime import datetime
from settings import get_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from db.database import User, Presentation

irids = list()
preses = list()

file = open("all_doklady.xml", "r", encoding="utf-8")
xml_file = file.read()
soup = BeautifulSoup(xml_file, features="xml")
settings = get_settings()
engine = create_engine(str(settings.DB_DSN))
with Session(bind=engine) as session:
    for tag in soup.find_all("presentation"):
        for creator in tag.find_all("creator"):
            result = re.match(r"([а-яА-Яa-zA-Zё .]+)(\d+)", creator.text)
            if not (result is None):
                creators_db = [int(user.irid) for user in session.query(User).all()]
                if int(result[2]) not in irids:
                    irids.append(int(result[2]))
                if int(result[2]) not in creators_db:
                    session.add(User(
                        irid=int(result[2]),
                        name=result[1]
                    ))
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
            created=datetime.strptime(tag.created.text, '%Y-%m-%d %H:%M:%S'),
            creators=irids
        )
        session.add(presentation)
        session.commit()

        irids = []
