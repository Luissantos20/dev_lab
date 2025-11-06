from typing import List

from app.schemas.task_schema import TaskCreate, TaskOut

# ---------------------------
# "Banco de dados" em memória
# ---------------------------
# Uma lista de dicts manterá as tasks.
# Cada item armazenado terá as chaves: id, title, description, done.
_tasks_storage: list[dict] = []

# Contador simples para gerar IDs únicos.
_next_id: int = 1


def list_tasks() -> List[TaskOut]:
    """
    Retorna todas as tasks como objetos TaskOut.
    Por que TaskOut? Porque é o contrato de saída da API.
    """
    return [TaskOut(**item) for item in _tasks_storage]


def create_task(payload: TaskCreate) -> TaskOut:
    """
    Cria uma nova task a partir de um TaskCreate validado pelo Pydantic.
    - Convertemos o payload (modelo) para dict.
    - Geramos um id.
    - Montamos o registro completo e validamos com TaskOut.
    - Guardamos em memória e retornamos o objeto final.
    """
    global _next_id

    data = payload.model_dump()  # Pydantic v2: vira dict tipado
    data["id"] = _next_id
    _next_id += 1

    # Validação final: garante que o registro completo respeita o contrato
    task = TaskOut(**data)

    # Persistência (em memória por enquanto)
    _tasks_storage.append(task.model_dump())

    return task
