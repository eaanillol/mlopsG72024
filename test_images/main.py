from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.post("/test")
def test():
    return {
        "status": 200,
        "message":"Test successful"
    }