from fastapi import FastAPI

app = FastAPI(title="AI Customer Support API")

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Customer Support API!"}
