from fastapi import FastAPI

app = FastAPI(title="IT Training System", version="0.2.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"service": "it-training-system-api", "docs": "/docs"}

from routes import training

app.include_router(training.router)
