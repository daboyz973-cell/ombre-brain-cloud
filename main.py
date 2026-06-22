from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

memory = []

class MemoryItem(BaseModel):
    text: str


@app.get("/")
def root():
    return {"message": "brain cloud online"}


@app.post("/remember")
def remember(item: MemoryItem):
    memory.append(item.text)
    return {
        "success": True,
        "count": len(memory)
    }


@app.get("/memories")
def memories():
    return {
        "memories": memory
    }
