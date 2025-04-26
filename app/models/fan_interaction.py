from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Representa um torcedor da FURIA
class Fan(BaseModel):
    id: int
    name: str
    age: Optional[int] = None  # Opcional se você não tiver certeza da idade
    favorite_player: Optional[str] = None  # Se em algum momento for obrigatório, remova o Optional
    created_at: datetime = datetime.now()

    # Método para atualizar o timestamp de criação se necessário
    def set_created_at(self):
        if not self.created_at:
            self.created_at = datetime.now()

# Representa uma interação (ex: uma pergunta ou mensagem)
class Interaction(BaseModel):
    fan_id: int  # referência ao ID do torcedor
    message: str
    timestamp: datetime = datetime.now()

    # Método para garantir o timestamp atual
    def set_timestamp(self):
        if not self.timestamp:
            self.timestamp = datetime.now()
