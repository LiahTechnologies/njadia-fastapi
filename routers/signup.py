
from datetime import datetime,timedelta
from logging import Logger
from beanie import Document, PydanticObjectId
from fastapi import APIRouter, Form, HTTPException
from jose import JWTError
from pydantic import BaseModel, ValidationError
from models.auth_model import MultipleValidationErrors, User,Login,Token
from typing import List, Type
from fastapi import UploadFile, File

# main.py
from fastapi import File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
from loguru import logger
from bson import ObjectId
from typing import List
from core.services import security
from core.services.status import status
from uuid import uuid4
import boto3
import magic
import key
# from fastapi import FormObject 

signupRouter = APIRouter()


# CONTSTANTS FOR THIS FILE


KB=1024
MB=1024*KB


SUPPORTED_TYPES ={
    "image/png":"png",
    "image/jpeg":"jpeg",
    "application/pdf":"pdf"
}


# HLEPER FUNCTIONS
# 

_AWS_BUCKET ='signup-bucket-njadia-001'


s3= boto3.resource("s3")
bucket = s3.Bucket(_AWS_BUCKET)


async def s3_upload(contents:bytes,key:str):
    # logger.info(f'uploading {key} to s3')
    bucket.put_object(Key=key,Body=contents)
    # pass
   




def validate_json(model: Type[Document]):
    def wrapper(body: str = Form(...)):
        try:
            return model.parse_raw(body)
        except ValidationError as exc:
            errors = exc.errors()
            for error in errors:
                error["loc"] = tuple(["body"] + list(error["loc"]))
            raise MultipleValidationErrors(errors)
            # raise ""

    return wrapper




@signupRouter.post("/signup")
async def signup(docs:UploadFile,selfie:UploadFile,data:User=Form(...)):
    # print(data)
    
    
  

    if not docs and not selfie:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail      = "FILES  NOT UPLOADED"
        )
    

   

    selfie_content = await selfie.read()
    docs_content   = await docs.read()
    
    selfie_size    = len(selfie_content)
    docs_size      = len(docs_content)

    if not 0<selfie_size<=1*MB and not 0<docs_content<=1*MB:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail      = "File size is too big"
        )
    

    file_types_selfie = magic.from_buffer(buffer=selfie_content,mime=True)
    file_types_docs    = magic.from_buffer(buffer=docs_content,mime=True)


    if file_types_docs not in SUPPORTED_TYPES and file_types_selfie not in SUPPORTED_TYPES:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail      = f"Unsupported file types {file_types_docs} and {file_types_selfie}. supported type {SUPPORTED_TYPES}"
        )
    selfie_key          = f'{uuid4()}.{SUPPORTED_TYPES[file_types_docs]}'
    docs_key            = f'{uuid4()}.{SUPPORTED_TYPES[file_types_selfie]}'

    await s3_upload(contents = docs_content , key = f'{uuid4()}.{SUPPORTED_TYPES[file_types_selfie]}')
    await s3_upload(contents = selfie_content, key = f'{uuid4()}.{SUPPORTED_TYPES[file_types_docs]}')
    


    # user_details=User(
    #     firstName=data.firstName,
    #     lastName=data.lastName,
    #     email=data.email,
    #     password=security.bycrypte_context.hash(data.password),
    #     tel=data.tel,
    #     dob=data.dob,
    #     selfie ="selfie_key",
    #      docs ="docs_key",
       
 
    #     )
    
    # {
    #     "firstName":data.firstName,
    #     "lastName":data.lastName,
    #     "email":data.email,
    #     "tel":data.tel,
    #     "dob":data.dob,
    #     "selfie_content":selfie_content,
    #     "selfie_name":selfie.filename,
    #     "selfie_type":selfie_type,
    #     "docs_type":docs_type,
    #     "docs_name":docs.filename,
    #     "docs_content":docs_content
    # }
  
    # user= await user_details.save()
    # user['id']=str(user['_id'])
    # del(user['_id']) 
    return {"message":f"User created successfully ","uid":""}





@signupRouter.post("/login")
async def login(data:Login):
    user =await authentication(data.email,data.password)

    print(f"\n\nTHIS IS THE CURRENT USER ${user}\n\n")

    if not user:
        raise HTTPException(status_code=404,detail="Not found")
    
    token = create_access_token(user.firstName,user.lastName,timedelta(minutes=20))

    return {"token":token,"token_type":"bearer"}

   

def create_access_token(username:str,user_id:PydanticObjectId,expire_delta:timedelta):
    encode= {"sub":username,"id":user_id}
    expires = datetime.utcnow()+expire_delta
    encode.update({'exp':expires})
    return security.jwt.encode(encode,security.SECRET_KEY,algorithm=security.ALGORITHM)


async def authentication(email:str,password:str):
    print(f"T\n\nHIS IS THE AUTHENTICATION PART \n\n")

    user = await User.find_one({"email":email})
    print(f"T\n\nHIS IS THE AUTHENTICATION PART OF THE APPPLICATION ${user}\n\n")
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found this")
    if not security.bycrypte_context.verify(password,user.password):
        return False
    return user



@signupRouter.delete("/users")
async def deleteusers():
    await User.delete_all()
    return {"message":"Users Deleted"}



@signupRouter.get("/users")
async def allUsers():
    users = await User.find_all().to_list()

    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Not found")

    return users



@signupRouter.get("/users/{email}")
async def getAUser(user_id:str):
    single_user = await User.find_one({"email":user_id})
    
    if not single_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="This user does not exist")
    
    return single_user





# uploading files to AWS S3
# 




