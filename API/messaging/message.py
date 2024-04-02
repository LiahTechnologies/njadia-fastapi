from fastapi import FastAPI, WebSocket, APIRouter,WebSocketDisconnect,WebSocketException
from .connection_manager import ConnectionManager


message = APIRouter()

connection_manager= ConnectionManager()



async def startup_connect():
    await connection_manager.connect()

@message.get("/messages")
async def messages():

        
    return {"messages":"THIS ARE THE MESSAGES OF THE APPLICATION"}

@message.websocket("/ws/{channel_id}/")

async def websocket_endpoint(channel_id:str, websocket:WebSocket):
    await websocket.accept()
    # add user to connectio stack

    await connection_manager.add_user_to_channel(channel_id=channel_id, websocket_connection=websocket)

    try:
        while True:
            data= await websocket.receive_json()
            print(f'this is the received message {data}')
            message = data['message']

            await connection_manager.send_message_to_channel(channel_id=channel_id,message=message)
    except WebSocketDisconnect:

        pass

    except WebSocketException as e:
        pass


   