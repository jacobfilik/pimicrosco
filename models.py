from pydantic import BaseModel
from enum import Enum


#'add_overlay'
#'analog_gain'
# 'annotate_background'
# 'annotate_foreground'
# 'annotate_frame_num'
# 'annotate_text'
# 'annotate_text_size'
# 'awb_gains'
# 'awb_mode'
# 'brightness'
# 'capture'
# 'capture_continuous
# 'capture_sequence'
# 'clock_mode'
# 'close'
# 'closed'
# 'color_effects'
# 'contrast'
# 'digital_gain',
# 'drc_strength'
# 'exif_tags',
# 'exposure_compensation',
# 'exposure_mode',
# 'exposure_speed',
# 'flash_mode',
# 'frame',
# 'framerate',
# 'framerate_delta',
# 'framerate_range',
# 'hflip',
# 'image_denoise',
# 'image_effect',
# 'image_effect_params',
# 'iso',
# 'led',
# 'meter_mode',
# 'overlays',
# 'preview',
# 'preview_alpha',
# 'preview_fullscreen',
# 'preview_layer',
# 'preview_window',
# 'previewing',
# 'raw_format',
# 'record_sequence',
# 'recording',
# 'remove_overlay',
# 'request_key_frame',
# 'resolution',
# 'revision', 'rotation',
# 'saturation', 'sensor_mode', 'sharpness', 'shutter_speed', 'split_recording',
# 'start_preview', 'start_recording', 'still_stats', 'stop_preview', 'stop_recording',
# 'timestamp', 'vflip', 'video_denoise', 'video_stabilization', 'wait_recording', 'zoom'

class AWBModeEnum(str, Enum):
    off = "off"
    auto = "auto"
    sunlight = 'sunlight'
    cloudy = 'cloudy'
    shade = 'shade'
    tungsten = 'tungsten'
    fluorescent = 'fluorescent'
    incandescent = 'incandescent'
    flash = 'flash'
    horizon = 'horizon'

class AWB(BaseModel):
    r_gain : float = 0
    b_gain : float = 0
    mode : AWBModeEnum = AWBModeEnum.auto

class Zoom(BaseModel):
    x : float = 0
    y : float = 0
    h : float = 1
    w : float = 1

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
