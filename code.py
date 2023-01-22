from photometer.photometer import Photometer
from photometer import constants

photometer = Photometer()

if not constants.IS_TEST:
    while True:
        photometer.loop()
