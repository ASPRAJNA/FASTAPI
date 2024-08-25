import uuid
from typing import Optional
from pydantic import BaseModel, Field, validator
from datetime import date
from bson import ObjectId

class AllTask(BaseModel):
    _id: str = Field(default_factory=uuid.uuid4, alias="_id")
    title: str 
    description: str 
    date : str
    user_id:str
    
    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "title": "My new Task 1",
                "description": "Need to complete my new task  as soon as possible",
                "date": "21-01-2000"
            }
        }

class Task(BaseModel):
    title:str
    description: str 
    date : str

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "title": "My new Task 1",
                "description": "Need to complete my new task  as soon as possible",
                "date": "21-01-2000"
            }
        }
    
class UpdateTask(BaseModel):
    title: Optional[str] 
    description: Optional[str]
    date: Optional[str]
    
    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "title": "My new Task 1 upadted",
                "description": "Need to complete my new task  as soon as possible updated",
                "date": "23-01-2000"
            }
        }
