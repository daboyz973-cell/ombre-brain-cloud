from fastapi import FastAPI

app = FastAPI()

memory = []


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/test")
def test():
    return {"message": "server is running"}


@app.post("/remember")
def remember(item: dict):
    memory.append(item.get("text", ""))
    return {"saved": True, "total": len(memory)}


@app.get("/memory")
def get_memory():
    return {"memory": memory}
