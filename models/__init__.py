from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import CONNECTION

engine = create_engine(CONNECTION)

Base = declarative_base()

Session = sessionmaker()
Session.configure(bind=engine)

session = Session()
