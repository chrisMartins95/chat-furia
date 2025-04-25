from fastapi import FastAPI
from pydantic import BaseModel
from app.models import Fan, Interaction  # importa os modelos que você criou

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}
