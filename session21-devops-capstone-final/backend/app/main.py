from fastapi import Depends, FastAPI, HTTPException, Response
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy import func, text
from sqlalchemy.orm import Session

from app.config import APP_NAME
from app.db import Base, engine, get_db
from app.models import Task
from app.schemas import TaskCreate, TaskOut, TaskStats, TaskUpdate

app = FastAPI(title=APP_NAME, version="1.0.0")
Instrumentator().instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)


@app.on_event("startup")
def create_local_tables() -> None:
    # Compose runs Alembic first; this keeps direct SQLite development friction-free.
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"service": "projectpulse-api", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/ready")
def ready(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
    except Exception as exc:
        raise HTTPException(status_code=503, detail="database unavailable") from exc
    return {"status": "ready", "database": "reachable"}


@app.get("/api/tasks", response_model=list[TaskOut])
def list_tasks(status: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Task)
    if status:
        query = query.filter(Task.status == status)
    return query.order_by(Task.created_at.desc()).all()


@app.get("/api/tasks/stats", response_model=TaskStats)
def task_stats(db: Session = Depends(get_db)):
    rows = dict(db.query(Task.status, func.count(Task.id)).group_by(Task.status).all())
    return TaskStats(total=sum(rows.values()), todo=rows.get("todo", 0), in_progress=rows.get("in_progress", 0), done=rows.get("done", 0))


@app.get("/api/tasks/{task_id}", response_model=TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    return task


@app.post("/api/tasks", response_model=TaskOut, status_code=201)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    task = Task(**payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@app.put("/api/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


@app.delete("/api/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    db.delete(task)
    db.commit()
    return Response(status_code=204)
