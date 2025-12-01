from typing import List, Optional

from fastapi import APIRouter, HTTPException, status

from app.schemas.task_schema import TaskCreate, TaskOut, TaskUpdate
from app.services.task_service import (
    create_task,
    delete_task,
    get_task,
    list_tasks,
    update_task,
)

# Criamos o router específico para "tasks"
router = APIRouter()


@router.get("/", response_model=List[TaskOut], status_code=status.HTTP_200_OK)
def get_tasks(
    done: Optional[bool] = None,
    q: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
):
    """
    Lista tasks com filtros opcionais:
    - done: filtra por status (true/false)
    - q: busca textual no título
    - paginação: skip e limit
    """
    return list_tasks(done=done, q=q, skip=skip, limit=limit)


@router.get(
    "/{task_id}",
    response_model=TaskOut,
    status_code=status.HTTP_200_OK,
)
def get_task_by_id(task_id: int):
    """
    Retorna uma única task pelo ID.
    Se não existir, responde com erro 404.
    """
    task = get_task(task_id)

    if task is None:
        # Dispara um erro HTTP 404 (Not Found)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


@router.put(
    "/{task_id}",
    response_model=TaskOut,
    status_code=status.HTTP_200_OK,
)
def update_task_by_id(task_id: int, payload: TaskUpdate):
    """
    Atualiza parcialmente uma task existente.
    Se a task não existir, retorna 404.
    """
    updated_task = update_task(task_id, payload)

    if updated_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return updated_task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task_by_id(task_id: int):
    """
    Remove uma task pelo ID.
    - Se a task não existir, responde 404.
    - Se remover com sucesso, responde 204 (sem conteúdo).
    """
    was_deleted = delete_task(task_id)

    if not was_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # 204 No Content → não precisa retornar corpo
    return None


@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def post_task(payload: TaskCreate):
    """
    Cria uma nova task com base no payload recebido.
    """
    # O FastAPI transforma o JSON recebido em um objeto TaskCreate.
    # Depois passamos esse objeto pro service.
    return create_task(payload)
