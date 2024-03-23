from fastapi  import FastAPI

from database import init_db
from API.signup import signup
from API import task 




app = FastAPI()

@app.on_event("startup")
async def connect():
    await init_db()




# app.include_router(task_router)
app.include_router(signup.signupRouter)


