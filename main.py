from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

conn = sqlite3.connect("brain.db", check_same_thread=False)
cursor = conn.cursor()


class MemoryItem(BaseModel):
    session_id: str
    text: str


@app.get("/")
def root():
    return {"status": "brain cloud v3.1 smart mode"}


# 写入
@app.post("/remember")
def remember(item: MemoryItem):
    cursor.execute(
        "INSERT INTO memory (session_id, text) VALUES (?, ?)",
        (item.session_id, item.text)
    )
    conn.commit()

    return {"ok": True}


# 读取全部
@app.get("/memory/{session_id}")
def get_memory(session_id: str):

    cursor.execute(
        "SELECT text FROM memory WHERE session_id=?",
        (session_id,)
    )

    data = [r[0] for r in cursor.fetchall()]

    return {
        "memory": data,
        "count": len(data)
    }


# 🧠 智能搜索（不需要AI）
@app.get("/search")
def search(q: str, session_id: str):

    cursor.execute(
        "SELECT text FROM memory WHERE session_id=?",
        (session_id,)
    )

    data = [r[0] for r in cursor.fetchall()]

    result = [m for m in data if q.lower() in m.lower()]

    return {
        "query": q,
        "results": result
    }


# 🧠 自动总结（简化版）
@app.get("/summary/{session_id}")
def summary(session_id: str):

    cursor.execute(
        "SELECT text FROM memory WHERE session_id=?",
        (session_id,)
    )

    data = [r[0] for r in cursor.fetchall()]

    return {
        "summary": "；".join(data[-5:])  # 最近5条
    }
