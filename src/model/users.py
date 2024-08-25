import uuid
from pydantic import BaseModel, Field, SecretStr
from pydantic.networks import EmailStr
from typing import Optional,Required

class User(BaseModel):
    _id: str = Field(default_factory=uuid.uuid4, alias="_id",index=True,unique=True)
    name: str 
    email: EmailStr = Field(unique=True)
    password: str    

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "name": "Prajna",
                "email": "asprajna@gmail.com",
                "password": "asprajna.psl.123",
            }
        }

class Register(BaseModel):
    name:str
    email:str
    password:str
    confirmpass:str

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "name": "Prajna",
                "email": "asprajna@gmail.com",
                "password": "asprajna.psl.123",
                "confirmpass":"asprajna.psl.123"
            }
        }

class Login(BaseModel):
    _id: str = Field(default_factory=uuid.uuid4, alias="_id",index=True,unique=True)
    email:str
    password:str
    
    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "email":"asprajna@gmail.com",
                "password":"asprajna.psl.123"
            }
        }


class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: Optional[str] = None

