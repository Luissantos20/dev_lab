from typing import List, Optional

from app.schemas.task_schema import TaskCreate, TaskOut, TaskUpdate

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


def get_task(task_id: int) -> Optional[TaskOut]:
    """
    Busca uma task pelo ID.
    - Se encontrar, retorna TaskOut.
    - Se não encontrar, retorna None.
    """
    for item in _tasks_storage:
        if item["id"] == task_id:
            # Valida e retorna a task encontrada
            return TaskOut(**item)
    # Se não achar nada, retorna None
    return None


def update_task(task_id: int, payload: TaskUpdate) -> Optional[TaskOut]:
    """
    Atualiza parcialmente uma task existente.
    - Se a task não existir, retorna None.
    - Se existir, mescla os dados antigos com os novos,
      valida com TaskOut, salva e retorna o objeto atualizado.
    """
    # 1) Procurar o índice da task no storage
    for index, item in enumerate(_tasks_storage):
        if item["id"] == task_id:
            # 2) Dados atuais da task
            current_data = item

            # 3) Dados enviados no payload, ignorando campos None
            update_data = {
                key: value
                for key, value in payload.model_dump().items()
                if value is not None
            }

            # 4) Mesclar os dados (os novos sobrescrevem os antigos)
            merged_data = {**current_data, **update_data}

            # 5) Validar o resultado final com TaskOut
            updated_task = TaskOut(**merged_data)

            # 6) Salvar de volta no storage (como dict)
            _tasks_storage[index] = updated_task.model_dump()

            # 7) Retornar o objeto atualizado
            return updated_task

    # Se não encontrar a task, retorna None
    return None


def delete_task(task_id: int) -> bool:
    """
    Remove uma task pelo ID.
    - Se remover com sucesso, retorna True.
    - Se não encontrar a task, retorna False.
    """
    for index, item in enumerate(_tasks_storage):
        if item["id"] == task_id:
            # Remove a task da lista pelo índice
            del _tasks_storage[index]
            return True

    # Se não encontrou nenhuma task com esse ID
    return False
