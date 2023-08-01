from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Response
import io
import asyncio
import base64
from models import Exposure,ISOEnum, ExpModeEnum,DRCEnum

app = FastAPI()


class ConnectionManager:
    def __init__(self):
        self.active_connections = []
        self.buffer = io.BytesIO()

    async def connect(self, websocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        #print("start task")
        asyncio.create_task(self.monitor(websocket))
        #print("task running")
 
    async def monitor(self, websocket):
        try:
            print("Waiting")
            await websocket.receive_text()
        except Exception as ex:
            print("Exception")
            
        self.active_connections.remove(websocket)

    def disconnect(self, websocket):
        print(f"Disconnect called on {websocket}")
        self.active_connections.remove(websocket)

    def set_loop(self,loop):
        self.loop = loop

    async def broadcast(self, message):
        for connection in self.active_connections:
            #print(connection.connected)
            #print((connection.client_state))
            await connection.send_bytes(message)

manager = ConnectionManager()


@app.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket):
    print((websocket.client_state))
    await manager.connect(websocket)
    buf = None
    with open("my_video.h264", "rb") as fh:
        buf = io.BytesIO(fh.read())

    while True and manager.active_connections:
        try:
            buf.seek(0)
            await asyncio.sleep(0.03)
            await manager.broadcast(buf)
    #except WebSocketDisconnect:
        except Exception as e:
            print(f"Exception {e}")
            manager.disconnect(websocket)


@app.get("/snapimage")
async def snap():
    headers = {"Content-type": "text/html"}
    with open("./image.jpg", 'rb') as fh:
        data = fh.read()
        data = base64.b64encode(data)


    res = Response(content=data, media_type="text/html")
    return res


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/data")
async def data():
    return {"text": "Hello World", "number": 15}



@app.get("/exposure")
async def exposure() -> Exposure:
    exp = Exposure()
    exp.iso = ISOEnum.iso100
    exp.analog_gain = 0.1
    exp.digital_gain = 0.2
    exp.exposure_speed = 0.3
    exp.shutter_speed = 0.4
    exp.compensation = 0.5
    exp.mode = ExpModeEnum.auto
    exp.drc_strength = DRCEnum.off
 
    return exp

@app.put("/setexp")
async def set_exposure(exp : Exposure) -> Exposure:
    print(exp)
    return exp
