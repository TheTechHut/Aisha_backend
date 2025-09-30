from sqlalchemy import Column, Integer, String
from database import Base

class WaitingList(Base):
    __tablename__ = "waiting_list"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    phone_number = Column(String, index=True) 