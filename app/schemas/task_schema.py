from typing import Optional

from pydantic import BaseModel, Field


# 1) Campos comuns a uma task: título, descrição e status
class TaskBase(BaseModel):
    # Field: define validações e metadados que vão parar na doc automática
    title: str = Field(
        ..., min_length=1, max_length=120, description="Título curto da tarefa"
    )
    description: Optional[str] = Field(
        default=None, max_length=500, description="Detalhes da tarefa"
    )
    done: bool = Field(default=False, description="Se a tarefa foi concluída")


# 2) Modelo de entrada para criação (POST) — herda tudo do base
class TaskCreate(TaskBase):
    """Payload para criar uma task"""


# 3) Modelo de entrada para atualização (PUT) — todos opcionais
class TaskUpdate(BaseModel):
    """Payload para atualizar uma task (campos parciais são permitidos)"""

    title: Optional[str] = Field(default=None, min_length=1, max_length=120)
    description: Optional[str] = Field(default=None, max_length=500)
    done: Optional[bool] = None


# 4) Modelo de saída para respostas da API — inclui id
class TaskOut(TaskBase):
    id: int = Field(..., description="Identificador único da task")
