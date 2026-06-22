from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import time

app = FastAPI()

# ====== 内存（先用临时版，后面再换数据库）======
memory = []


# ====== Claude 输入结构 ======
class ClaudeRequest(BaseModel):
    user_text: str
    session_id: Optional[str] = "default"


# ====== 写入记忆 ======
@app.post("/claude/remember")
def claude_remember(req: ClaudeRequest):
    memory.append({
        "text": req.user_text,
        "session_id": req.session_id,
        "time": time.time()
    })

    return {
        "status": "ok",
        "saved": req.user_text,
        "total": len(memory)
    }


# ====== Claude 读取记忆 ======
@app.get("/claude/memory")
def claude_memory(session_id: str = "default"):
    result = [
        m for m in memory
        if m["session_id"] == session_id
    ]

    return {
        "session_id": session_id,
        "memory": result,
        "count": len(result)
    }


# ====== 健康检查 ======
@app.get("/")
def root():
    return {
        "status": "claude brain cloud running"
    }
