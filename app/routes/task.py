from fastapi import APIRouter, Depends, Path, HTTPException

from app.dependencies.authentication import get_current_user
from app.models import User, TaskDetail, TaskCreate, Task, TaskFullDetail
from app.tasks import process_task

task_router = APIRouter()


@task_router.post("/task", tags=['Task'])
async def create_task(task_data: TaskCreate, user: User = Depends(get_current_user)) -> TaskDetail:
    """
       Create a new task using the provided task data and the authenticated user.
       The function takes in the task data (TaskCreate) and the authenticated user (User)
       as parameters and returns a TaskDetail object.
    """

    new_task = Task.create(**task_data.dict())
    task_detail = TaskDetail(id=new_task.id)
    process_task.apply_async(args=[task_data.ip, new_task.id], countdown=1)
    return task_detail


@task_router.get("/status/{id}", tags=['Task'])
async def get_task_status(id: int = Path(..., title="The ID of the task"),
                    user: User = Depends(get_current_user)) -> TaskFullDetail:
    """
      Get the status of a task.
      Parameters:
          id (int): The ID of the task.
          user (User): The current user.
      Returns:
          TaskFullDetail: The detailed information of the task.
    """

    task = Task.select().where(Task.id == id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task_detail = TaskFullDetail(**task.to_dict())
    return task_detail
