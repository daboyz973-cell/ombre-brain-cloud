from fastapi import FastAPI

app = FastAPI(return)

@app.get("/")
def read_root():
    return {"message": "brain cloud is running"}
