import json
import time
from datetime import datetime
import requests

ON_URL = "http://217.208.122.15/socket1On"
OFF_URL = "http://217.208.122.15/socket1Off"

active = True

lastOnTime = "Never turned on"
lastOffTime = "Never turned off"

while active:
    now = datetime.now()
    f = open("Lampsettings.json")
    settings = json.load(f)
    f.close()

    for t in settings["on_times"]:
        if now.hour == t["h"] and now.minute == t["m"]:
            requests.get(url=ON_URL)
            lastOnTime = now.strftime("%H:%M:%S")

    for t in settings["off_times"]:
        if now.hour == t["h"] and now.minute == t["m"]:
            requests.get(url=OFF_URL)
            lastOffTime = now.strftime("%H:%M:%S")

    active = settings["active"]

    f = open("lamps.log", "w")
    f.write(now.strftime("%H:%M:%S")
            + "\nlast ON:" + lastOnTime
            + "\nlast OFF:" + lastOffTime
            )
    f.close()

    time.sleep(10)


