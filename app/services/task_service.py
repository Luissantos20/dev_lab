from typing import List, Optional

from fastapi import HTTPException, status

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
    Cria uma nova tarefa a partir de um objeto TaskCreate validado pelo Pydantic.

    Etapas executadas:
    - Normaliza o título e descrição removendo espaços extras.
    - Valida título não vazio após strip().
    - Impede criação de títulos duplicados (case-insensitive).
    - Gera um ID único incremental.
    - Monta os dados finais, valida com TaskOut e salva no armazenamento.

    Retorna:
        TaskOut: A tarefa criada já validada pelo schema de saída.

    Lança:
        HTTPException(400): caso o título seja vazio ou duplique outro existente.
    """
    global _next_id

    # --- Normalização dos campos ---
    title = payload.title.strip()
    description = payload.description.strip() if payload.description else None

    # --- Validação: título não pode ser vazio após strip ---
    if title == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title cannot be empty or whitespace.",
        )

    # --- Validação: título não pode duplicar outro existente ---
    for item in _tasks_storage:
        if item["title"].lower() == title.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Task title already exists.",
            )

    # --- Montagem do registro limpo ---
    data = {
        "id": _next_id,
        "title": title,
        "description": description,
        "done": payload.done,
    }
    _next_id += 1

    # --- Validação final com schema de saída ---
    task = TaskOut(**data)

    # --- Persistência em memória ---
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
    Atualiza parcialmente uma tarefa existente.

    Etapas executadas:
    - Procura a task pelo ID.
    - Normaliza campos enviados (strip).
    - Valida título não vazio após strip().
    - Impede atualização para título duplicado (case-insensitive).
    - Mescla dados antigos com novos.
    - Valida o conjunto final com TaskOut.
    - Salva no armazenamento e retorna.

    Retorna:
        TaskOut: caso a task seja atualizada.
        None: caso a task não exista.

    Lança:
        HTTPException(400): se o título for inválido ou duplicado.
    """
    # --- 1) Procurar a task pelo ID ---
    for index, item in enumerate(_tasks_storage):
        if item["id"] == task_id:

            # Dados atuais da task
            current_data = item.copy()

            # Dados enviados no payload (ignorando campos não informados)
            update_data = {
                key: value
                for key, value in payload.model_dump().items()
                if value is not None
            }

            # --- Validações avançadas ---

            # Título: normalização + validações
            if "title" in update_data:
                new_title = update_data["title"].strip()

                if new_title == "":
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Title cannot be empty or whitespace.",
                    )

                # Impedir duplicidade de título (exceto a própria task)
                for other in _tasks_storage:
                    if (
                        other["id"] != task_id
                        and other["title"].lower() == new_title.lower()
                    ):
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Task title already exists.",
                        )

                update_data["title"] = new_title

            # Descrição: aplicar strip se enviada
            if "description" in update_data and update_data["description"] is not None:
                update_data["description"] = update_data["description"].strip()

            # --- 4) Mesclar dados: novos > antigos ---
            merged_data = {**current_data, **update_data}

            # --- 5) Validar resultado final com schema de saída ---
            updated_task = TaskOut(**merged_data)

            # --- 6) Persistir no armazenamento ---
            _tasks_storage[index] = updated_task.model_dump()

            return updated_task

    # Task não encontrada
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
