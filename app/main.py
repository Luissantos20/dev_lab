from fastapi import FastAPI

from app.routers.tasks import router as tasks_router

app = FastAPI(title="Dev Lab API", version="0.1.0")


@app.get("/")
def read_root():
    return {"message": "🚀 Ambiente configurado com sucesso!"}


# Inclui as rotas de tasks com prefixo /tasks
app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
