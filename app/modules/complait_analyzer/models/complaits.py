# pylint: disable=E1136
from datetime import datetime

from sqlalchemy.orm import (
    mapped_column
)
from sqlalchemy import String, Integer, JSON, Text, Enum, DateTime
from database.base import Base
from modules.complait_analyzer.schemas.payload import Sentiment, Status, Category


# Base tables
class Complaits(Base):
    __tablename__ = "complaits"
    id = mapped_column(Integer, primary_key= True, autoincrement=True)
    text = mapped_column(Text, nullable=False)
    status  = mapped_column(Enum(Status, values_callable=lambda x: [e.value for e in x]), default=Status.open.value)
    timestamp = mapped_column(DateTime,  default=datetime.now())
    sentiment = mapped_column(Enum(Sentiment, values_callable=lambda x: [e.value for e in x]), default=Sentiment.neutral.value)
    category = mapped_column(Enum(Category, values_callable=lambda x: [e.value for e in x]), default=Category.other.value)
    geolocation = mapped_column(JSON, nullable=False)
    
    


    
    
    



    
    
    
    
    
    