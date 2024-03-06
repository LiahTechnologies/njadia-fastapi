
from fastapi import APIRouter



signupRouter = APIRouter()



@signupRouter.get("/login")
async def signup():
    pass




@signupRouter.post("/signup")
async def login():
    pass


@signupRouter.get("/auth")
async def authentication():
    pass


