from fastapi import FastAPI

app = FastAPI(title="IT Training API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def root():
    return {"service": "it-training-api", "docs": "/docs"}
