
from fastapi import APIRouter
from auth_model import Signup



signupRouter = APIRouter()



@signupRouter.post("/login")
async def signup(data:Signup):
    await data.create()
    return {"message":"User created successfully"}





@signupRouter.post("/signup")
async def login():
    pass


@signupRouter.get("/auth")
async def authentication():
    pass


