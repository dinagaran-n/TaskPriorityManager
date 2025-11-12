from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import os, json, uuid

app = FastAPI(title="Task Priority Manager")

# Allow frontend to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data file outside backend folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data.json")

def load_data():
    try:
        with open(DATA_PATH, "r") as f:
            text = f.read().strip()
            if not text:
                print("⚠️ data.json empty — reinitializing.")
                save_data([])
                return []
            return json.loads(text)
    except json.JSONDecodeError:
        print("⚠️ data.json corrupted — resetting to empty list.")
        save_data([])
        return []
    except Exception as e:
        print("⚠️ Unexpected error reading data.json:", e)
        return []

def save_data(data):
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)

# Models
class Task(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    priority: int = Field(3, ge=1, le=5)
    status: str = "PENDING"
    due_date: Optional[str] = None
    created_at: str
    updated_at: str

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: int = Field(3, ge=1, le=5)
    status: Optional[str] = "PENDING"
    due_date: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    priority: Optional[int]
    status: Optional[str]
    due_date: Optional[str]

# Endpoints
@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return load_data()

@app.post("/tasks", response_model=Task)
def create_task(task: TaskCreate):
    data = load_data()
    new_task = Task(
        id=str(uuid.uuid4()),
        title=task.title,
        description=task.description,
        priority=task.priority,
        status=task.status or "PENDING",
        due_date=task.due_date,
        created_at=datetime.utcnow().isoformat(),
        updated_at=datetime.utcnow().isoformat(),
    )
    data.append(new_task.dict())
    save_data(data)
    return new_task

@app.patch("/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, updates: TaskUpdate):
    data = load_data()
    for task in data:
        if task["id"] == task_id:
            for k, v in updates.dict(exclude_unset=True).items():
                task[k] = v
            task["updated_at"] = datetime.utcnow().isoformat()
            save_data(data)
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    data = load_data()
    new_data = [t for t in data if t["id"] != task_id]
    save_data(new_data)
    return {"deleted": len(data) != len(new_data)}

@app.on_event("startup")
def startup():
    print(f"✅ Server started. Using data file: {DATA_PATH}")
