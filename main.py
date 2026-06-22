from fastapi import FastAPI
from pydantic import BaseModel
import time

app = FastAPI()

memory = []


class ChatRequest(BaseModel):
    text: str
    session_id: str = "default"


# ===== 写入记忆 =====
@app.post("/remember")
def remember(req: ChatRequest):
    memory.append({
        "text": req.text,
        "session_id": req.session_id,
        "time": time.time()
    })

    return {
        "status": "saved",
        "total": len(memory)
    }


# ===== 读取记忆 =====
@app.get("/memory")
def get_memory(session_id: str = "default"):
    data = [
        m for m in memory
        if m["session_id"] == session_id
    ]

    return {
        "memory": data
    }


# ===== 模拟“AI回复”（Claude替代版）=====
@app.post("/chat")
def chat(req: ChatRequest):

    # 找相关记忆
    related = [
        m["text"] for m in memory
        if req.text in m["text"] or m["text"] in req.text
    ]

    reply = "我记住了你的话。"

    if related:
        reply += " 我想起你之前说过：" + "；".join(related[:3])

    return {
        "reply": reply,
        "memory_used": len(related)
    }


# ===== 健康检查 =====
@app.get("/")
def root():
    return {"status": "brain cloud v2 running"}
        "status": "claude brain cloud running"
    }
