from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

memory = []

class MemoryItem(BaseModel):
    text: str

@app.get("/")
def root():
    return {"message": "brain cloud is running"}

@app.post("/remember")
def remember(item: MemoryItem):
    memory.append(item.text)
    return {"ok": True, "total": len(memory)}

@app.get("/memories")
def get_memories():
    return {"memory": memory}
