import picamera
from picamera import PiCamera, PiVideoFrameType
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Response
import io
from io import BytesIO
import base64
import asyncio
from pydantic import BaseModel
from enum import Enum

class AWBModeEnum(str, Enum):
    off = "off"
    auto = "auto"

class AWB(BaseModel):
    r_gain : float = 0
    b_gain : float = 0
    mode : AWBModeEnum = AWBModeEnum.auto

class Zoom(BaseModel):
    x0 : float = 0
    x1 : float = 1
    y0 : float = 0
    y1 : float = 1

class Resolution(BaseModel):
    width : int = 1920
    height : int = 1080

class ExpModeEnum(str,Enum):
    auto = 'auto'
    off = 'off'
    night = 'night'
    nightpreview = 'nightpreview'
    backlight = 'backlight'
    spotlight = 'spotlight'
    sports = 'sports'
    snow = 'snow'
    beach = 'beach'
    verylong = 'verylong'
    fixedfps = 'fixedfps'
    antishake = 'antishake'
    fireworks = 'fireworks'

class DRCEnum(str, Enum):
    off = "off"
    low = "low"
    medium = "medium"
    high = "high"

class MeterModeEnum(str,Enum):
    average = 'average'
    spot = 'spot'
    backlit = 'backlit'
    matrix = 'matrix'

class ISOEnum(int,Enum):
    iso000 = 0
    iso100 = 100
    iso200 = 200
    iso320 = 320
    iso400 = 400
    iso500 = 500
    iso640 = 640
    iso800 = 800

class Exposure(BaseModel):
    compensation : int = 0
    mode : ExpModeEnum = ExpModeEnum.auto
    exposure_speed : int = 0
    shutter_speed : int = 0
    iso : ISOEnum = ISOEnum.iso100
    digital_gain : float = 0.0
    analog_gain : float = 0.0
    drc_strength : DRCEnum = DRCEnum.off

class CameraModel(BaseModel):
    awb : AWB = AWB()
    brightness : int = 50
    contrast : int = 0
    digital_gain : float = 1.46
    drc_strength : DRCEnum = DRCEnum.off
    exposure : Exposure = Exposure()
    framerate :  int = 0
    framerate_delta : int = 0
    iso : int = 0
    meter_mode : MeterModeEnum = MeterModeEnum.average
    rotation : int = 0
    saturation : int = 0
    shutter_speed : int = 0
    resolution : Resolution = Resolution()
    zoom : Zoom = Zoom()

#        status["awb_gains"] = (float(r),float(b))


#        status["awb_mode"] = camera.awb_mode
#        status["brightness"] = camera.brightness
#        status["constrast"] = camera.contrast
#        status["digital_gain"] = float(camera.digital_gain)
#        status["drc_strength"] = camera.drc_strength
#        status["exposure_compensation"] = camera.exposure_compensation
#        status["exposure_mode"] = camera.exposure_mode
#        status["exposure_speed"] = camera.exposure_speed
#        status["framerate"] = float(camera.framerate)
#        status["framerate_delta"] = float(camera.framerate_delta)
#        status["iso"] = camera.iso
#        status["meter_mode"] = camera.meter_mode
#        res = camera.resolution
#        status["resolution"] = (res.width, res.height)
#        status["rotation"] = camera.rotation
#        status["saturation"] = camera.saturation
#        status["shutter_speed"] = camera.shutter_speed
#        status["zoom"] = camera.zoom


#{
#  "awb_gains": [
#    2.78125,
#    1.94921875
#  ],
#  "awb_mode": "auto",
#  "brightness": 50,
#  "constrast": 0,
#  "digital_gain": 1.4609375,
#  "drc_strength": "off",
#  "exposure_compensation": 0,
#  "exposure_mode": "auto",
#  "exposure_speed": 32979,
#  "framerate": 30,
#  "framerate_delta": 0,
#  "iso": 0,
#  "meter_mode": "average",
#  "resolution": [
#    1920,
#    1080
#  ],
#  "rotation": 0,
#  "saturation": 0,
#  "shutter_speed": 0,
#  "zoom": [
#    0,
#    0,
#    1,
#    1
#  ]
#}

camera = PiCamera(sensor_mode=2, resolution='1920x1080', framerate=30)
camera.video_denoise = False

recordingOptions = {
    'format' : 'h264', 
    'quality' : 20, 
    'profile' : 'high', 
    'level' : '4.2', 
    'intra_period' : 15, 
    'intra_refresh' : 'both', 
    'inline_headers' : True, 
    'sps_timing' : True
}

class StreamBuffer(object):
    def __init__(self,camera):
        self.frameTypes = PiVideoFrameType()
        self.buffer = io.BytesIO()
        self.camera = camera


    def write(self, buf):
        if self.camera.frame.complete and self.camera.frame.frame_type != self.frameTypes.sps_header:
            self.buffer.write(buf)
            if self.loop is not None and wsHandler.hasConnections():
                self.loop.add_callback(callback=wsHandler.broadcast, message=self.buffer.getvalue())
            self.buf.seek(0)
            self.buffer.seek(0)
            self.buffer.truncate()
        else:
            self.buffer.write(buf)

class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket):
        self.active_connections.remove(websocket)


    async def broadcast(self, message):
        for connection in self.active_connections:
            await connection.send_bytes(message)

class CameraConnectionManager:
    def __init__(self,camera):
        self.active_connections = []
        self.frameTypes = PiVideoFrameType()
        self.camera = camera
        self.buffer = io.BytesIO()

    async def connect(self, websocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket):
        self.active_connections.remove(websocket)

    def set_loop(self,loop):
        self.loop = loop

    def write(self,buf):
        if self.camera.frame.complete and self.camera.frame.frame_type != self.frameTypes.sps_header:

            self.buffer.write(buf)
            asyncio.run_coroutine_threadsafe(self.broadcast(self.buffer.getvalue()),self.loop)
            self.buffer.seek(0)
            self.buffer.truncate()
        else:
            self.buffer.write(buf)

    async def broadcast(self, message):
        for connection in self.active_connections:
            await connection.send_bytes(message)

manager = ConnectionManager()
camManager = CameraConnectionManager(camera)
app = FastAPI()

@app.on_event("shutdown")
def shutdown_event():
    print("Exit")


@app.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket):
    print(camManager)
    camManager.set_loop(asyncio.get_event_loop())
    await camManager.connect(websocket)

    camera.start_recording(camManager, **recordingOptions) 
    buf = None
    try:
        while True:
            await asyncio.sleep(0.01)
    except WebSocketDisconnect:
        camManager.disconnect(websocket)

@app.websocket("/ws2/")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    buf = None
    with open("my_video.h264", "rb") as fh:
        buf = io.BytesIO(fh.read())
    try:
        while True:
            buf.seek(0)
            await asyncio.sleep(0.01)
            await manager.broadcast(buf)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.put("/update")
async def update(camera : CameraModel) -> CameraModel:
    print(camera)
    return camera


@app.get("/status2")
async def status2() -> CameraModel:
    cam = CameraModel()

    r,b = camera.awb_gains
    cam.awb = AWB()
    cam.awb.r_gain = r
    cam.awb.b_gain = b
    cam.brightness = camera.brightness
    cam.contrast = camera.contrast
    cam.digital_gain = float(camera.digital_gain)
#    exposure : Exposure = Exposure()
#    framerate :  int = 0
#    framerate_delta : int = 0
#    iso : int = 0
#    meter_mode : MeterModeEnum = MeterModeEnum.average
#    rotation : int = 0
#    saturation : int = 0
#    shutter_speed : int = 0
#    resolution : Resolution = Resolution()
#    zoom : Zoom = Zoom()
    return cam

@app.get("/exposure")
async def exposure() -> Exposure:
    exp = Exposure()
    exp.iso = camera.iso
    exp.analog_gain = float(camera.analog_gain)
    exp.digital_gain = float(camera.digital_gain)
    exp.exposure_speed = camera.exposure_speed
    exp.shutter_speed = camera.shutter_speed
    exp.compensation = camera.exposure_compensation
    exp.mode = camera.exposure_mode
    exp.drc_strength = camera.drc_strength
 
    return exp


@app.get("/test")
async def root():
    return {"message": "Hello World"}


@app.put("/awb")
async def put_awb(awb : AWB) -> AWB:

    payload = AWB()
    print(awb)
    camera.awb_mode = awb.mode
    camera.awb_gains = (awb.r_gain, awb.b_gain)

    r,b = camera.awb_gains
    payload.mode = camera.awb_mode
    payload.r_gain = r
    payload.b_gain = b

    return payload

@app.get("/status")
async def status():
        status = {}
        r,b = camera.awb_gains
        status["awb_gains"] = (float(r),float(b))
        status["awb_mode"] = camera.awb_mode
        status["brightness"] = camera.brightness
        status["constrast"] = camera.contrast
        status["digital_gain"] = float(camera.digital_gain)
        status["drc_strength"] = camera.drc_strength
        status["exposure_compensation"] = camera.exposure_compensation
        status["exposure_mode"] = camera.exposure_mode
        status["exposure_speed"] = camera.exposure_speed
        status["framerate"] = float(camera.framerate)
        status["framerate_delta"] = float(camera.framerate_delta)
        status["iso"] = camera.iso
        status["meter_mode"] = camera.meter_mode
        res = camera.resolution
        status["resolution"] = (res.width, res.height)
        status["rotation"] = camera.rotation
        status["saturation"] = camera.saturation
        status["shutter_speed"] = camera.shutter_speed
        status["zoom"] = camera.zoom
        return status

@app.get("/snap")
async def snap():
    headers = {"Content-type": "text/html"}
    with open("./image.jpg", 'rb') as fh:
        data = fh.read()
        data = base64.b64encode(data)


    res = Response(content=data, media_type="text/html")
    return res

@app.get("/snapimage")
def snapimage():

    headers = {"Content-type": "text/html"}

    stream = BytesIO()
        #self.add_header("Content-Type",header)
    camera.capture(stream,'jpeg')
    return Response(content=base64.b64encode(stream.getvalue()).decode(), media_type="text/html")

@app.get("/snapimagejpg")
def snapimage():


    stream = BytesIO()
        #self.add_header("Content-Type",header)
    camera.capture(stream,'jpeg')
    return Response(content=stream.getvalue(), media_type="image/jpeg")
