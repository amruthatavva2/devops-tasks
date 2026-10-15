def task_payload(**overrides):
    payload = {"title": "Prepare release checklist", "description": "Confirm every pipeline gate", "status": "todo", "priority": "high", "owner": "Amrutha"}
    payload.update(overrides)
    return payload


def test_health_and_ready(client):
    assert client.get("/health").json()["status"] == "healthy"
    assert client.get("/ready").json()["database"] == "reachable"


def test_create_and_get_task(client):
    created = client.post("/api/tasks", json=task_payload())
    assert created.status_code == 201
    task_id = created.json()["id"]
    fetched = client.get(f"/api/tasks/{task_id}")
    assert fetched.status_code == 200
    assert fetched.json()["title"] == "Prepare release checklist"


def test_list_tasks_and_filter(client):
    client.post("/api/tasks", json=task_payload(status="todo"))
    client.post("/api/tasks", json=task_payload(title="Release application", status="done"))
    assert len(client.get("/api/tasks").json()) == 2
    assert len(client.get("/api/tasks?status=done").json()) == 1


def test_update_task(client):
    task_id = client.post("/api/tasks", json=task_payload()).json()["id"]
    response = client.put(f"/api/tasks/{task_id}", json={"status": "in_progress", "priority": "critical"})
    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"
    assert response.json()["priority"] == "critical"


def test_stats_and_delete_task(client):
    task_id = client.post("/api/tasks", json=task_payload()).json()["id"]
    client.post("/api/tasks", json=task_payload(title="Publish metrics", status="done"))
    assert client.get("/api/tasks/stats").json() == {"total": 2, "todo": 1, "in_progress": 0, "done": 1}
    assert client.delete(f"/api/tasks/{task_id}").status_code == 204
    assert client.get(f"/api/tasks/{task_id}").status_code == 404


def test_rejects_invalid_title(client):
    response = client.post("/api/tasks", json=task_payload(title="x"))
    assert response.status_code == 422
