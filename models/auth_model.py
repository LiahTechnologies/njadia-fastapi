


from typing import List, Type, Union, Any, Dict, Tuple, TypedDict
from pydantic import ValidationError
from beanie import Document
from fastapi import UploadFile, File
from fastapi.types import UnionType
# models.py
from pydantic import BaseModel


class User(Document):
    firstName:str
    lastName:str
    email:str
    password:str
    tel:int
    dob:str
    selfie:str
    docs:str
   

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
            "selfie":"",
            "docs":""
        }




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

Loc = Tuple[Union[int, str], ...]
class _ErrorDictRequired(TypedDict):
    loc: Loc
    msg: str
    type: str

class ErrorDict(_ErrorDictRequired, total=False):
    ctx: Dict[str, Any]

class MultipleValidationErrors(Exception):
    def __init__(self, errors: List[ErrorDict]):
        super().__init__()
        self.errors = errors
