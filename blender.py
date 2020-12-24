import sys
import os
import threading
import importlib

import bpy

sys.path.append(os.path.dirname(bpy.data.filepath))

import neopixel
importlib.reload(neopixel)
xmaslights = __import__("xmaslights-spin")
importlib.reload(xmaslights)
xmaslights.coordfilename = os.path.join(os.path.dirname(bpy.data.filepath),"coords.txt")

duration_seconds = 10
def stop_after_duration():
    import time
    time.sleep(duration_seconds)
    xmaslights.run=0

if __name__ == "__main__":
    stop_thread = threading.Thread(target=stop_after_duration)
    #Create the LED objects before starting the timer
    pixels = neopixel.NeoPixel()
    stop_thread.start()
    xmaslights.run=1
    xmaslights.xmaslight()
    stop_thread.join()
