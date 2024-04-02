from typing import Set,Dict
from fastapi import WebSocket 
import asyncio
import traceback
from starlette.websockets import WebSocketState
from broadcaster import Broadcast
class ConnectionManager:
    
    def __init__(self):
        self.connections: Dict[str,Set[WebSocket]] = {}
        self.broadcast =Broadcast("redis://localhost:6379")



    async def connect(self):
        await self.broadcast.connect()

    async def disconnect(self):
         await self.broadcast.disconnect()

    # async def send_personal_message(self, message: str, websocket: WebSocket):
    #     await websocket.send_text(message)

    # async def broadcast(self, message: str):
    #     for connection in self.active_connections:
    #         await connection.send_text(message)


    async def  _send_message_to_channel(self,channel_id: str,message:str):
        if channel_id not in self.connections.keys():
            return 
        
        for connection in self.connections[channel_id]:
            await self.send_message_to_ws_connection(message= f'Channel::{channel_id}->{message}',ws_connection=connection)



    
    async def send_message_to_ws_connection(self,message:str,ws_connection:WebSocket)->bool:
            try:
                await ws_connection.send_text(message)
                return True,"Message sent"
            except RuntimeError:
                return False,"Message  Not Sent, WebSocket is disconnected"
            except Exception as e:
                traceback.print_exc()

                return False, "Error Sending Message"
            
    


    def remove_user_connection(self, user_id):
        pass
            



    async def add_user_to_channel(self,channel_id:str, websocket_connection:WebSocket):

        if channel_id not in self.connections.keys():

            self.connections[channel_id]={websocket_connection}

            subscribe_task= asyncio.create_task(self._subscribbed_to_channel(channel_id=channel_id))

            wait_task= asyncio.create_task(asyncio.sleep(1))

            await asyncio.wait([subscribe_task,wait_task],return_when=asyncio.FIRST_COMPLETED)

             

        else :
            self.connections[channel_id].add(websocket_connection)

            return True, "Connection Successful"
        

        
    async def send_message_to_channel(self,channel_id:str, message:str):
        
        await self.broadcast.publish(channel=channel_id, message=message)



    
    async def _subscribbed_to_channel(self,channel_id:str):
        async with self.broadcast.subscribe(channel=channel_id) as subscriber:
            async for event in subscriber:
                await self._send_message_to_channel(channel_id=channel_id,message=event.message)
                




    async def check_if_a_connection_still_active(self, ws_connection:WebSocket,message=".")->bool:

        
            if not(ws_connection.application_state==WebSocketState.CONNECTED and ws_connection.client_state):
                return False
            


            try:
                await ws_connection.send_text(message)
            except RuntimeError:
                return False
            except Exception as e:
                traceback.print_exc()
                return False
            return True

   
        