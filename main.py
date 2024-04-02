from fastapi  import FastAPI

from database import init_db
from API.signup import signup
from API import task 
from API.messaging import message




app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await init_db()
    await  message.startup_connect()
    print("CONNECTED TO REDIS SUCCESSFULLY")


@app.on_event("shutdown")
async def shutdown():
   await message.connection_manager.disconnect()

# app.include_router(task_router)
app.include_router(signup.signupRouter)
app.include_router(message.message)


