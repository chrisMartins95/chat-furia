from fastapi import FastAPI

app = FastAPI(title="FURIA Tech Challenge – Chat Bot")

@app.get("/health")
def health():
    return {"status": "ok"}
