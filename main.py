from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, List

app = FastAPI()

# session -> memory
db: Dict[str, List[str]] = {}


class MemoryItem(BaseModel):
    session_id: str
    text: str


@app.get("/")
def root():
    return {"status": "multi-device brain cloud running"}


# 写入记忆（支持多设备）
@app.post("/remember")
def remember(item: MemoryItem):

    if item.session_id not in db:
        db[item.session_id] = []

    db[item.session_id].append(item.text)

    return {
        "ok": True,
        "session": item.session_id,
        "total": len(db[item.session_id])
    }


# 读取记忆（多设备同步关键）
@app.get("/memory/{session_id}")
def get_memory(session_id: str):

    return {
        "session": session_id,
        "memory": db.get(session_id, [])
    }
