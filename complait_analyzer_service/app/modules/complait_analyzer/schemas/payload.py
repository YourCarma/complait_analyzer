from typing import Optional
from datetime import datetime
import enum

from pydantic import BaseModel, Field


class Status(enum.Enum):
    open = "open"
    closed = "closed"
    
class Sentiment(enum.Enum):
    positive = "positive"
    negative = "negative"
    neutral = "neutral"
    unknown = "unknown"
    
class Category(enum.Enum):
    technical = "техническая"
    payment = "оплата"
    other = "другое"
    
    
class ComplaitCreation(BaseModel):
    text: str = Field(
        description="Заголовок задачи", examples=["У меня не работает СМС"]
    )
    
class Complait(BaseModel):
    id: int = Field(
        description="ID задачи", examples=[1, 2]
    )
    text: str = Field(
        description="Текст жалобы", examples=["СМС не работает :("]
    )
    timestamp: datetime = Field(
        description="Дата создания записи", examples=[datetime.now()]
    )
    status: Status = Field(
        description="Жалоба открыта выполнена", examples=[Status.open]
    )
    sentiment: Sentiment = Field(
        description="Тональность жалобы", examples=[Sentiment.negative]
    )
    category: Category = Field(
        description="Категория жалобы", default=Category.other.value, examples=[Category.other]
    )
    geolocation: str = Field(
        description="Геолокация жалобы по IP"
    )
    class Config:
        json_encoders = {
            enum.Enum: lambda v: v.value
        }
        use_enum_values = True
    
class ComplaitCreationResponse(BaseModel):
    id: int = Field(
        description="ID задачи", examples=[1, 2]
    )
    status: Status = Field(
        description="Жалоба открыта выполнена", examples=[Status.open]
    )
    sentiment: Sentiment = Field(
        description="Тональность жалобы", examples=[Sentiment.negative]
    )
    category: Category = Field(
        description="Категория жалобы", default=Category.other.value, examples=[Category.other]
    )
    geolocation: str = Field(
        description="Геолокация жалобы по IP"
    )
    class Config:
        json_encoders = {
            enum.Enum: lambda v: v.value
        }
        use_enum_values = True
        
class ChangeComplaitStatus(BaseModel):
    id: int = Field(
        description="ID задачи", examples=[1, 2]
    )
    status: Status = Field(
        description="Жалоба открыта выполнена", examples=[Status.open]
    )
    
    