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


@router.get(
    "/",
    response_model=List[TaskOut],
    summary="Lista todas as tarefas",
    description=(
        "Retorna todas as tarefas cadastradas. "
        "Permite aplicar filtros por status (done), "
        "busca textual no título (q) e paginação (skip, limit)."
    ),
)
def get_tasks(
    done: Optional[bool] = None,
    q: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
):
    """
    Lista tarefas existentes.

    **Parâmetros**:

    - **done**: Filtra por tarefas concluídas (`true`) ou não concluídas (`false`).
    - **q**: Busca textual no título da tarefa.
    - **skip**: Quantidade de itens a pular (paginação).
    - **limit**: Quantidade máxima de itens retornados.

    Retorna uma lista de `TaskOut`.
    """
    return list_tasks(done=done, q=q, skip=skip, limit=limit)


@router.get(
    "/{task_id}",
    response_model=TaskOut,
    status_code=status.HTTP_200_OK,
    summary="Obtém uma tarefa específica",
    description="Busca e retorna uma tarefa única pelo seu identificador.",
)
def get_task_by_id(task_id: int):
    """
    Retorna uma única tarefa pelo ID.

    **Possíveis erros:**
    - **404**: caso a tarefa não exista.
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
    summary="Atualiza uma tarefa existente",
    description=(
        "Atualiza parcialmente uma tarefa. "
        "Apenas os campos enviados serão modificados."
    ),
)
def update_task_by_id(task_id: int, payload: TaskUpdate):
    """
    Atualiza parcialmente uma tarefa.

    Possíveis erros:
    - **404**: tarefa não encontrada
    - **400**: título vazio após strip
    - **400**: título duplicado
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
    summary="Remove uma tarefa",
    description="Remove uma tarefa do armazenamento pelo ID.",
)
def delete_task_by_id(task_id: int):
    """
    Apaga uma task pelo ID.

    Possíveis erros:
    - **404**: tarefa não encontrada.
    """
    was_deleted = delete_task(task_id)

    if not was_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # 204 No Content → não precisa retornar corpo
    return None


@router.post(
    "/",
    response_model=TaskOut,
    status_code=status.HTTP_201_CREATED,
    summary="Cria uma nova tarefa",
    description="Cria uma tarefa validada e persiste no armazenamento.",
)
def post_task(payload: TaskCreate):
    """
    Cria uma nova tarefa.

    Possíveis erros:
    - **400**: título vazio após strip
    - **400**: título duplicado
    - **422**: erro de validação do payload
    """
    return create_task(payload)
