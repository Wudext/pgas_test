from settings import get_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from db.database import User, Patent
import xlsxwriter

settings = get_settings()
engine = create_engine(str(settings.DB_DSN))
objects = []
with Session(bind=engine) as session:
    patents = session.query(Patent).all()
    for patent in patents:
        users = patent.creators
        for user in users:
            name = session.query(User).filter(User.irid == user).one_or_none().name
            objects.append([name, user, len(users), str(patent.date), str(patent.created)])

with xlsxwriter.Workbook('patents.xlsx') as workbook:
    worksheet = workbook.add_worksheet()

    for row_num, data in enumerate(objects):
        worksheet.write_row(row_num, 0, data)
