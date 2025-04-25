from pydantic import BaseModel
from datetime import datetime

class Message(BaseModel):
    user: str
    message: str
    timestamp: datetime = datetime.now()
