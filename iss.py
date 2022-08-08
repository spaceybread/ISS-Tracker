from urllib.request import urlopen
import json
from datetime import *
import pytz
from tzwhere import tzwhere
from timezonefinder import TimezoneFinder

doLog = input('Log session? (y/n) \n')

initReq = urlopen("http://api.open-notify.org/iss-now.json").read()
initObj = json.loads(initReq)

name = initObj['timestamp']

while True:

    tzf = TimezoneFinder()

    req = urlopen("http://api.open-notify.org/iss-now.json").read()

    obj = json.loads(req)

    latt = float(obj['iss_position']['latitude'])
    long = float(obj['iss_position']['longitude'])

    timezoneISS = tzf.timezone_at(lat=latt, lng=long)

    print(obj['timestamp'])
    print(str(latt) + ', ' + str(long))

    print(str(timezoneISS))

    localTime = datetime.now(pytz.timezone(timezoneISS))
    print('Local time: {}:{}'.format(localTime.hour,localTime.minute))

    if doLog == 'y':
        dict = {
            "timestamp": obj['timestamp'],
            "latitude": latt,
            "longitude": long,
            "timezone": timezoneISS,
            "l_hr": str(localTime.hour),
            "l_min": str(localTime.minute),
        }

        with open('Session UT {}.json'.format(name), 'a') as f:
            json.dump(dict, f)


    if int(localTime.hour) <= 6 or int(localTime.hour) >= 19:
        print('The ISS is cruising through the dark night! Sweet trails!')
    else:
        print("The ISS is riding across the bright sky! It's always sunny up there!")
