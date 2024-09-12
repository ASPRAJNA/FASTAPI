import uuid
from typing import Optional
from pydantic import BaseModel


class Task(BaseModel):
    title:str
    description: str 

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "title": "My new Task 1",
                "description": "Need to complete my new task  as soon as possible",
            }
        }
    
class UpdateTask(BaseModel):
    title: Optional[str] 
    description: Optional[str]
    
    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "title": "My new Task 1 upadted",
                "description": "Need to complete my new task  as soon as possible updated",
            }
        }
