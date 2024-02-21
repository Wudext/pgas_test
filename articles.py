from bs4 import BeautifulSoup
import re
from datetime import datetime
from settings import get_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from db.database import User, Article

irids = list()
creators_db = list()

file = open("all_articles_irid.xml", "r", encoding="utf-8")
xml_file = file.read()
soup = BeautifulSoup(xml_file, features="xml")
settings = get_settings()
engine = create_engine(str(settings.DB_DSN))
with Session(bind=engine) as session:
    for tag in soup.find_all("article"):
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

        article = Article(
            title=tag.title.text,
            publicationName=tag.publicationName.text,
            issn=tag.issn.text if tag.issn else None,
            doi=tag.doi.text if tag.doi else None,
            journalRanking_value=float(tag.journalRanking.text) if tag.journalRanking else None,
            journalRanking_type=tag.journalRanking["type"] if tag.journalRanking else None,
            journalRanking_year=tag.journalRanking["year"] if tag.journalRanking else None,
            publisher=tag.publisher.text,
            publicationDate=tag.publicationDate.text,
            publicationID=tag.ID.text,
            url=tag.url.text,
            is_vak=tag.is_vak.text,
            is_WoS=tag.is_WoS.text,
            is_Scopus=tag.is_Scopus.text,
            is_RINC=tag.is_RINC.text,
            val_WoS=int(tag.val_WoS.text) if tag.val_WoS else None,
            val_Scopus=int(tag.val_Scopus.text) if tag.val_Scopus else None,
            created=datetime.strptime(tag.created.text, '%Y-%m-%d %H:%M:%S'),
            attachments=tag.attachments.text if tag.attachments else None,
            creators=irids
        )
        session.add(article)
        session.commit()

        irids = []
