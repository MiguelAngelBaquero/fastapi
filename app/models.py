from sqlalchemy import Column, Integer, String, Date
from database import Base

class Movie(Base):
  __tablename__ = 'my_movies'
  
  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  author = Column(String, index=True, nullable=True)
  description = Column(String, index=True, nullable=False, unique=True)
  release_date = Column(Date, index=False, nullable=True)