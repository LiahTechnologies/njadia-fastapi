


from beanie import Document
from fastapi import UploadFile, File
# models.py
from pydantic import BaseModel


class User(Document):
    firstName:str
    lastName:str
    email:str
    password:str
    tel:int
    dob:str
    # selfie_content:bytes
    # selfie_name:str
    # selfie_type:str
    # docs_type:str
    # docs_name:str
    # docs_content:bytes

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
            # "selfie":File,
            # "docs":File
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
