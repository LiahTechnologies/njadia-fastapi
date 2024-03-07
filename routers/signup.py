
from datetime import datetime,timedelta
from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException
from jose import JWTError
from models.auth_model import User,Login,Token
from typing import List
from fastapi import UploadFile, File

# main.py
from fastapi import File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse

from bson import ObjectId
from typing import List
from core.services import security
from core.services.status import status

signupRouter = APIRouter()



@signupRouter.post("/signup")
async def signup(data:User):

    
    # selfie_content = await selfie.read()
    # selfie_type = selfie.content_type

    # docs_content = await docs.read()
    # docs_type = docs.content_type


    user_details=User(
        firstName=data.firstName,
        lastName=data.lastName,
        email=data.email,
        password=security.bycrypte_context.hash(data.password),
        tel=data.tel,
        dob=data.dob,
        # selfie_content=selfie_content,
        # selfie_name=selfie.filename,
        # selfie_type=selfie_type,
        # docs_type=docs_type,
        # docs_name=docs.filename,
        # docs_content=docs_content
        
        )
    
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
  
    await user_details.save()
    
    return {"message":f"User created successfully " }





@signupRouter.post("/login/{id}")
async def login(user_id:PydanticObjectId,userName:str):
    user =await authentication(user_id,userName)

    print(f"\n\nTHIS IS THE CURRENT USER ${user}\n\n")

    if not user:
        raise HTTPException(status_code=404,detail="Not found")
    
    token = create_access_token(userName,user.lastName,timedelta(minutes=20))

    return {"token":token,"token_type":"bearer"}

   

def create_access_token(username:str,user_id:PydanticObjectId,expire_delta:timedelta):
    encode= {"sub":username,"id":user_id}
    expires = datetime.utcnow()+expire_delta
    encode.update({'exp':expires})
    return security.jwt.encode(encode,security.SECRET_KEY,algorithm=security.ALGORITHM)


async def authentication(user_id:PydanticObjectId,userName:str):
    print(f"T\n\nHIS IS THE AUTHENTICATION PART \n\n")

    user = await User.get(user_id)
    print(f"T\n\nHIS IS THE AUTHENTICATION PART OF THE APPPLICATION ${user}\n\n")
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found this")
    if not security.bycrypte_context.verify(userName,user.password):
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
async def getAUser(user_id:PydanticObjectId):
    single_user = await User.get(user_id)
    
    if not single_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="This user does not exist")
    
    return single_user






