
from datetime import datetime,timedelta
from logging import Logger
from beanie import Document, PydanticObjectId
from dotenv import load_dotenv
from fastapi import APIRouter, Form, HTTPException,status
from jose import JWTError
from pydantic import BaseModel, ValidationError
from models.auth_model import OTP, VERIFY_OTP, User,Login,Token
from typing import List, Optional, Type
from fastapi import UploadFile, File

# main.py
from fastapi import File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
from loguru import logger
from bson import ObjectId
from typing import List
from core.services import security
from uuid import uuid4
import boto3
import magic
import os
from twilio.rest import Client
from dotenv import load_dotenv
import os
# from fastapi import FormObject 

signupRouter = APIRouter()


load_dotenv()

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
   


@signupRouter.post("/signup_files")
async def signup(
    docs:UploadFile,
    selfie:UploadFile,
                 ):
    
    if not docs and not selfie:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail      = "FILES  NOT UPLOADED"
        )
    
    selfie_content = await selfie.read()
    docs_content   = await docs.read()
    
    selfie_size    = len(selfie_content)
    docs_size      = len(docs_content)

    # if not 0<selfie_size<=1*MB and not 0<docs_size<=1*MB:
    #     raise HTTPException(
    #         status_code = status.HTTP_403_FORBIDDEN,
    #         detail      = "File size is too big"
    #     )
    

    file_types_selfie = magic.from_buffer(buffer=selfie_content,mime=True)
    file_types_docs    = magic.from_buffer(buffer=docs_content,mime=True)


    if file_types_docs not in SUPPORTED_TYPES and file_types_selfie not in SUPPORTED_TYPES:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail      = f"Unsupported file types {file_types_docs} and {file_types_selfie}. supported type {SUPPORTED_TYPES}"
        )
    selfie_key          = f'{uuid4()}.{SUPPORTED_TYPES[file_types_docs]}'
    docs_key            = f'{uuid4()}.{SUPPORTED_TYPES[file_types_selfie]}'

    await s3_upload(contents = docs_content , key = docs_key)
    await s3_upload(contents = selfie_content, key = selfie_key)
    


    return {"message":f"User created successfully ","selfie":selfie_key,"docs":docs_key}



@signupRouter.post("/signup_details")
async def signupDetail(data:User):
    print(f"THE USER DATA IS {data}")

    user_detail= User(
        firstName=data.firstName,
        lastName=data.lastName,
        email=data.email,
        tel=data.tel,
        dob=data.dob,
        selfie=data.selfie,
        docs=data.docs,
        password=security.bycrypte_context.encrypt(data.password)
    )
    user= await user_detail.save()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,data="User not created")
    return {"message":"User created successfully","user":user}



@signupRouter.post("/login")
async def login(data:Login):
    print(f"DATA FROM FRONTEND {data}")
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







@signupRouter.post("/otp")
async def otp_code(number:OTP):

    
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_ACCOUNT_TOKEN']
    verify_sid = os.environ['TWILIO_ACCOUNT_VERIFICATION_ID']



    verified_number = "+237"+number.number

    client = Client(account_sid, auth_token)

    verification = client.verify.v2.services(verify_sid) \
    .verifications \
    .create(to=verified_number, channel="sms")
    print(verification.status)

    

    return {"message":"code has been sent"}




@signupRouter.post("/verify")
async def verify_otp_code(code:VERIFY_OTP):
    
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_ACCOUNT_TOKEN']
    verify_sid = os.environ['TWILIO_ACCOUNT_VERIFICATION_ID']

   
    verified_number = "+237"+code.number

    client = Client(account_sid, auth_token)
    
    verification_check = client.verify.v2.services(verify_sid) \
    .verification_checks \
    .create(to=verified_number, code=code.code)
    print(verification_check.status)
    if verification_check.status != "approved":
        return {"message":"verification failed"}

    return {"message":"verification completed"}

