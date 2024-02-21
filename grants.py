from bs4 import BeautifulSoup
from datetime import datetime
from settings import get_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from db.database import User, Grant

irids = list()
grants = list()

date_len = (float(datetime(2023, 2, 1).strftime('%s')), float(datetime(2024, 1, 31).strftime('%s')))

file = open("all_grant.xml", "r", encoding="utf-8")
xml_file = file.read()
soup = BeautifulSoup(xml_file, features="xml")
settings = get_settings()
engine = create_engine(str(settings.DB_DSN))
with Session(bind=engine) as session:
    for tag in soup.find_all("project"):
        value = 0
        stages = [stage for stage in tag.find_all("stage")]
        relevant_stages = []
        for stage in stages:
            stage_begin = float(datetime.strptime(stage["begin"], "%d.%m.%Y").strftime('%s'))
            stage_end = float(datetime.strptime(stage["end"], "%d.%m.%Y").strftime('%s'))

            if (stage_begin < date_len[1]) or (stage_end > date_len[0]):
                relevant_stages.append(stage)
                for participant in stage.find_all("participant"):
                    creators_db = [int(user.irid) for user in session.query(User).all()]
                    if int(participant["irid"]) not in irids:
                        irids.append(int(participant["irid"]))
                    if int(participant["irid"]) not in creators_db:
                        session.add(User(
                            irid=int(participant["irid"]),
                            name=participant.fullname.text
                        ))
                        session.commit()
                for estimate in stage.find_all("estimates"):
                   value += int(estimate.value.text if estimate.value else 0)

        grant = Grant(
            title=tag.title.text,
            number=tag.number.text,
            dates_begin=datetime.strptime(relevant_stages[-1]["begin"], '%d.%m.%Y'),
            dates_end=datetime.strptime(relevant_stages[-1]["end"], '%d.%m.%Y'),
            department=tag.department.text,
            value=value,
            created=datetime.strptime(tag.created.text, '%Y-%m-%d %H:%M:%S'),
            creators=irids
        )
        session.add(grant)
        session.commit()

        irids = []
