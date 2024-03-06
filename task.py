
from beanie import PydanticObjectId
from model import Task
from fastapi import APIRouter, HTTPException
from typing import List


task_router = APIRouter()

# This is to get all task.
@task_router.get("/")
async def getalltask():
    tasks = await Task.find_all().to_list()
    return tasks


#  This to create a task 
@task_router.post("/task")
async def createtask(task:Task):
    new_taks = await task.create()

    return new_taks

    


#  
@task_router.get("/{task_id}")
async def retrieveTask(task_id:PydanticObjectId):
    located_task =await Task.get(task_id)
    return located_task
    


# This is to update a task
@task_router.put("/")
async def updateTask(task_id:PydanticObjectId, task:Task):

    updated = await Task.get(task_id)
    if not updated:
        raise HTTPException(status_code=404,detail="Not found")
    
    updated.task_content=task.task_content
    # updated.is_complete= task.is_complete,
    # updated.date_created = task.date_created

    await updated.save()

    return updated




# This is to delete a task
@task_router.delete("/")
async def deleteTask():
    await Task.delete_all()

    return{"message":"Data deleted"}