from fastapi import FastAPI

app = FastAPI(title="Dev Lab API", version="0.1.0")


@app.get("/")
def read_root():
    return {"message": "🚀 Ambiente configurado com sucesso!"}
