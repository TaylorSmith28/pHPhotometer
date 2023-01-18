"""
The file for the Photomter driver
"""
from photometer.photometer import Photometer

photometer = Photometer()

while True:
    photometer.loop()