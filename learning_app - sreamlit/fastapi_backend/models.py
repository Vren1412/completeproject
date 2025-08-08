from sqlalchemy import Column, Integer, String
from .database import Base  # Use relative import

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True)
    name = Column(String)
    password = Column(String)
    preferences = Column(String, nullable=True)
    course_interest = Column(String, nullable=True)
