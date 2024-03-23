


import json
from typing import List, Optional, Type, Union, Any, Dict, Tuple, TypedDict
from pydantic import ValidationError
from beanie import Document
from fastapi import status,Form
from fastapi.types import UnionType
from fastapi.exceptions import HTTPException
# models.py
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

class User(Document):
    firstName:str
    lastName:str
    email:str
    password:str
    tel:int
    dob:str
    selfie:str
    docs:str
    # args:Optional[str]
   

# def checker(data: str = Form(...)):
#     try:
#         return User.model_validate_json(data)
#     except ValidationError as e:
#         raise HTTPException(
#             detail=jsonable_encoder(e.errors()),
#             status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         )

    class settings:
        table_name="signup"

    
    class Config:
        extra_data={
            "firstName":"John Doe",
            "lastName":"Mac",
            "email":"example@gmail.com",
            "password":"wodjdjd234jdjkljs23",
            "tel":"3354666444",
            "dob":"12/03/1555",
            "selfie":"jk",
            "docs":"lkjkj"
        }




# def checker(data: str = Form(...)):
#     try:
#        return json.loads(data)
#     except json.JSONDecodeError:
#         raise HTTPException(status_code=400, detail='Invalid JSON data')



class File(BaseModel):
    filename: str
    content_type: str
    content: bytes


class Login(Document):
    email:str
    password:str


class Token(Document):
    token_type:str
    access_token:str



class OTP(Document):
    number:str


class VERIFY_OTP(Document):
    number:str
    code:int

