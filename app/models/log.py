from sqlalchemy import Column, Integer, String, JSON, Float
from app.config.database import Base




class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    timestamp = Column(String)
    method = Column(String)
    path = Column(String)
    query_params = Column(JSON)
    status_code = Column(Integer)
    response = Column(JSON)
    response_time = Column(Float)
