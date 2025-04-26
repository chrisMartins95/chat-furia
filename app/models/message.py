from pydantic import BaseModel
from datetime import datetime

class Message(BaseModel):
    user: str  # Pode ser alterado para user_id ou outro tipo, se necessário
    message: str
    timestamp: datetime = None  # Caso você queira passar explicitamente ou deixar o valor None

    # Método para garantir o timestamp atual se não passado explicitamente
    def set_timestamp(self):
        if not self.timestamp:
            self.timestamp = datetime.now()
