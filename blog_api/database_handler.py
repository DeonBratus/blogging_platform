from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://debral:12481632@localhost:5432/postgres"

engine = create_engine(DATABASE_URL)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class BlogDB(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True, index=True)
    article_title = Column(String, nullable=True)
    publishing_date = Column(Date, nullable=True)
    content = Column(String, nullable=True)

class UsersDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=True)
    password = Column(String)

Base.metadata.create_all(bind=engine)

def get_database():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
