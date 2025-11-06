from typing import List

from fastapi import APIRouter, status

from app.schemas.task_schema import TaskCreate, TaskOut
from app.services.task_service import create_task, list_tasks

# Criamos o router específico para "tasks"
router = APIRouter()


# ---------------------------------------
# Rota GET /tasks
# ---------------------------------------
@router.get("/", response_model=List[TaskOut], status_code=status.HTTP_200_OK)
def get_tasks():
    """
    Retorna todas as tasks salvas (em memória).
    """
    # Aqui só delegamos pro service.
    # O router não sabe "como" listar, só pede o resultado.
    return list_tasks()


# ---------------------------------------
# Rota POST /tasks
# ---------------------------------------
@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def post_task(payload: TaskCreate):
    """
    Cria uma nova task com base no payload recebido.
    """
    # O FastAPI transforma o JSON recebido em um objeto TaskCreate.
    # Depois passamos esse objeto pro service.
    return create_task(payload)
