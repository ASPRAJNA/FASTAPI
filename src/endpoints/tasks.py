from fastapi import APIRouter, Request, status,HTTPException,Depends
from src.endpoints.auth_beare import JWTBearer
from typing import List
from src.model.tasks import Task, UpdateTask,CreateTask
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
import uuid
from src.endpoints.auth_beare import get_current_user_id


jwt=JWTBearer()
dependency_JWT=[Depends(jwt)]

def get_collection_task(request: Request):
  return request.app.database["Tasks"]


router = APIRouter(prefix="/Tasks",
    tags=["Tasks"])

@router.post("/", response_description="Create Task", dependencies=dependency_JWT, status_code=status.HTTP_201_CREATED, response_model=CreateTask)
def create_task(request: Request, task: CreateTask):
    tasks = jsonable_encoder(task)
    global current_user
    current_user=get_current_user_id()
    tasks["user_id"]=str(current_user)
    new_task= get_collection_task(request).insert_one(tasks)
    created_task = get_collection_task(request).find_one({"_id": new_task.inserted_id})
    return created_task


@router.put("/{id}/", response_description="Update Task", dependencies=dependency_JWT, response_model=Task)
def update_task(request: Request, id: str, task: UpdateTask):
    tasks = {k: v for k, v in task.dict().items() if v is not None}
    print(tasks)
    if len(tasks) >= 1:
        update_result = get_collection_task(request).update_one({"_id": ObjectId(id)}, {"$set": tasks})
        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task not found!")
    if (existing_book := get_collection_task(request).find_one({"_id": ObjectId(id)})) is not None:
        return existing_book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"task not found!")



@router.get("/", response_description="All Tasks", response_model=List[Task])
def list_task(request: Request,limit:int):
    global current_user
    current_user=get_current_user_id()
    print(current_user)
    task = list(get_collection_task(request).find({"user_id":current_user}).limit(limit))
    return task


@router.get("/{id}/", response_description="Fetch Task By ID", response_model=Task)
def list_task_by_id(request: Request, id: str):
    if (task := get_collection_task(request).find_one({"_id": ObjectId(id)})):
        return task
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task not found!")


@router.delete("/{id}",  dependencies=dependency_JWT, response_description="Delete Task")
def delete_task(request: Request, id: str):
    deleted_task = get_collection_task(request).delete_one({"_id": ObjectId(id)})
    if deleted_task.deleted_count == 1:
        return f"Task with ID {id} deleted sucessfully!"
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task not found!")


