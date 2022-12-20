import math
import time

from pyicloud import PyiCloudService

TIMEOUT = 10  # seconds
HOME_COORDINATES = [
    35.863087,  # latitude
    -78.717367  #longitude
]
LATTITUDE_DISTANCE = 288200  # feet
IN_RANGE_OF_HOME = 1000  # feet

class Iphone:
    def __init__(self, credentials={}):
        self._client = PyiCloudService(**credentials)
        self._device = [
            i 
            for i in self._client.devices
            if i.content['id'] == '5yAbrrC4uESKPxpqfqHYlZocVy9SV5zvi7mxiFvihSk='
        ][0]
        self._home = None
    
    def isHome(self):
        latest_loc = self._device.location()
        if latest_loc['isInaccurate']:
            print("Location is inaccurate, cannot determine location")
            return None
        elif latest_loc['isOld']:
            print("Location is old, cannot determine location")
            return None
        else:
            for i in range(TIMEOUT):
                if latest_loc['locationFinished']:
                    break
                latest_loc = self._device.location()
                print(f"Location not finished {i}/{TIMEOUT}")
                time.sleep(1)
            else:
                print("Location never finished")
                return None
            
            lat = latest_loc['latitude']
            long = latest_loc['longitude']
            
            # difference between two points:
            # sqrt((x2 - x1)^2 - (y2 - y1)^2)
            
            # longitude is x, latitude is y
            
            distance = math.sqrt((long - HOME_COORDINATES[1])**2 - (lat - HOME_COORDINATES[0])**2)
            
            # 1 unit of longitude is 288,200 feet
            home = distance * LATTITUDE_DISTANCE < IN_RANGE_OF_HOME
            if self._home is None:
                self._home = home
            elif self._home is True and home is False:
                print("You have left home!")
            elif self._home is False and home is True:
                print("You have arrived home!")
            
            print(f"You are {'' if home else 'not '}home!")
            
            return home