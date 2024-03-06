from fastapi  import FastAPI

from task import task_router
from database import init_db
from routers import signup




app = FastAPI()

@app.on_event("startup")
async def connect():
    await init_db()




app.include_router(task_router)
app.include_router(signup.signupRouter)


