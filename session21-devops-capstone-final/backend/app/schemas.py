from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

TaskStatus = Literal["todo", "in_progress", "done"]
TaskPriority = Literal["low", "medium", "high", "critical"]


class TaskCreate(BaseModel):
    title: str = Field(min_length=2, max_length=160)
    description: str | None = Field(default=None, max_length=2000)
    status: TaskStatus = "todo"
    priority: TaskPriority = "medium"
    owner: str = Field(default="Unassigned", min_length=2, max_length=80)


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=160)
    description: str | None = Field(default=None, max_length=2000)
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    owner: str | None = Field(default=None, min_length=2, max_length=80)


class TaskOut(TaskCreate):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class TaskStats(BaseModel):
    total: int
    todo: int
    in_progress: int
    done: int
