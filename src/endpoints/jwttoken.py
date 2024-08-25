import os
from datetime import datetime, timedelta
from bson import ObjectId,json_util
import json
from dotenv import dotenv_values
from typing import Optional
import time
from jose import jwt
config = dotenv_values(".env")
current_user_id=None

JWT_SECRET_KEY=config["JWT_SECRET_KEY"]
ALGORITHM=config["ALGORITHM"]


def create_access_token(_id:dict):
    expires= time.time() + 1000
    to_encode = json.loads(json_util.dumps({"exp":expires ,"_id":ObjectId(_id['_id'])}))
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt
    

def decode_jwt(token: str) :
    try:
        decoded_token = jwt.decode(token, JWT_SECRET_KEY, ALGORITHM)
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except:
        return {}


