from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from typing import List

app = FastAPI()

# ======================
# 数据库初始化
# ======================
conn = sqlite3.connect("brain.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    text TEXT
)
""")
conn.commit()


# ======================
# 数据模型
# ======================
class MemoryItem(BaseModel):
    session_id: str
    text: str


# ======================
# 根接口
# ======================
@app.get("/")
def root():
    return {"status": "brain cloud v3 (persistent)"}


# ======================
# 写入记忆（永久存储）
# ======================
@app.post("/remember")
def remember(item: MemoryItem):

    cursor.execute(
        "INSERT INTO memory (session_id, text) VALUES (?, ?)",
        (item.session_id, item.text)
    )
    conn.commit()

    return {
        "ok": True,
        "session": item.session_id
    }


# ======================
# 读取记忆（多设备同步）
# ======================
@app.get("/memory/{session_id}")
def get_memory(session_id: str):

    cursor.execute(
        "SELECT text FROM memory WHERE session_id=?",
        (session_id,)
    )

    rows = cursor.fetchall()

    return {
        "session": session_id,
        "memory": [r[0] for r in rows]
    }
