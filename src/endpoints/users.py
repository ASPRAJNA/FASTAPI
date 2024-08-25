from fastapi import APIRouter, Request, status,HTTPException ,Depends
from typing import List
from src.model.users import User,Login,Register,Token
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
from src.endpoints.auth_beare import JWTBearer
from datetime import datetime, timedelta
from bson import ObjectId
from src.endpoints.jwttoken import create_access_token,decode_jwt

current_user_id=""
def get_collection_task(request: Request):
  return request.app.database["Users"]


router = APIRouter(prefix="/User",
    tags=["User"])

bcrypt_context = CryptContext(schemes =["bcrypt"],deprecated="auto")

@router.post("/register", response_description="Register", status_code=status.HTTP_201_CREATED, response_model=User)
def register_user(request: Request, user:Register):
    if(user.confirmpass!=user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Password And confirm password not Matched")
    existing_user = get_collection_task(request).find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail=f"Email already registered")
    hashed_password=bcrypt_context.hash(user.password)
    user_object = dict(user)
    new=user_object
    new["password"] = hashed_password
    new.pop('confirmpass')
    new_user= get_collection_task(request).insert_one(new)
    created_user = get_collection_task(request).find_one({"_id": new_user.inserted_id})
    return created_user


@router.post('/login', response_description="Login",response_model=Token)
def login( request:Request , user:Login):
    log_user =  get_collection_task(request).find_one({"email": user.email})  
    if not log_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f'No user found with this {user.email} email')
    if not bcrypt_context.verify(user.password,log_user["password"]):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f'Wrong Username or password')
    access_token = create_access_token({"_id":log_user["_id"] })
    return {"access_token": access_token, "token_type": "bearer"}


