

from datetime import datetime
from beanie import Document
from pydantic import Field



class Task(Document):
    task_content:str=Field(max_length=400)
    is_complete:bool
    date_created:datetime

    class Settings:
        name="task_database"

    class Config:
        schema_extra={
            "task_content":"This is a sample content",
            "is_complete":True,
            "date_created":datetime.now()
        }

