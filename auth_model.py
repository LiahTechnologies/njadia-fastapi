


from beanie import Document
from fastapi import UploadFile

class Signup(Document):
    firstName:str
    lastName:str
    email:str
    password:str
    tel:int
    dob:str
    selfie:UploadFile
    docs:UploadFile

    class settings:
        table_name="signup"

    
    class Config:
        extra_data={
            "firstName":"John Doe",
            "lastName":"Mac",
            "email":"example@gmail.com",
            "password":"wodjdjd234jdjkljs23",
            "tel":3354666444,
            "dob":"12/03/1555",
            "selfie":UploadFile,
            "docs":UploadFile
        }
