from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="Test API",
    description="API de test pour vérifier la configuration FastAPI",
    version="1.0.0"
)

class Message(BaseModel):
    message: str
    status: Optional[str] = None

@app.get("/", tags=["test"])
async def root():
    """
    Endpoint racine
    """
    return Message(
        message="Hello World",
        status="ok"
    )

@app.get("/test", tags=["test"])
async def test():
    """
    Endpoint de test
    """
    return Message(
        message="Test OK",
        status="ok"
    )
