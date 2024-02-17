from settings import get_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from db.database import User, Presentation


settings = get_settings()
engine = create_engine(str(settings.DB_DSN))
with Session(bind=engine) as session:
    users = session.query(User).all()
    print(len(users))
    preses = session.query(Presentation).all()
    print(len(preses))
