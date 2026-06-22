from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# ====== 内存（临时记忆）======
memory = []


# ====== 数据结构 ======
class MemoryItem(BaseModel):
    text: str


# ====== 根路径 ======
@app.get("/")
def root():
    return {"message": "brain cloud is running"}


# ====== 写入记忆 ======
@app.post("/remember")
def remember(item: MemoryItem):
    memory.append(item.text)
    return {
        "success": True,
        "total_memories": len(memory)
    }


# ====== 读取记忆 ======
@app.get("/memories")
def get_memories():
    return {
        "memories": memory
    }


# ====== 测试接口 ======
@app.get("/chat")
def chat(q: str = ""):
    return {
        "reply": "我收到了：" + q,
        "memory_count": len(memory)
    }
