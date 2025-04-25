from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Representa um torcedor da FURIA
class Fan(BaseModel):
    id: int
    name: str
    age: Optional[int] = None
    favorite_player: Optional[str] = None
    created_at: datetime = datetime.now()

# Representa uma interação (ex: uma pergunta ou mensagem)
class Interaction(BaseModel):
    fan_id: int  # referência ao ID do torcedor
    message: str
    timestamp: datetime = datetime.now()
