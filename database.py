# this file will be responsible to connect to mongodb

import beanie
import motor
import motor.motor_asyncio
from models.model import Task
from models.auth_model import User,Login



# connect to mongodb
async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")

    await beanie.init_beanie(
        database= client.db_name,
        document_models=[User,Login])