from urllib.request import urlopen
import json
import csv
from datetime import *
import pytz
from tzwhere import tzwhere
from timezonefinder import TimezoneFinder

doLog = input('Log session? (y/n) \n')

initReq = urlopen("http://api.open-notify.org/iss-now.json").read()
initObj = json.loads(initReq)

name = initObj['timestamp']

if doLog == 'y':
    with open('Session UT {}.csv'.format(name), 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'latitude', 'longitude', 'timezone', 'l_hr', 'l_min'])
        f.close()

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
        dict = [
            obj['timestamp'],
            latt,
            long,
            timezoneISS,
            str(localTime.hour),
            str(localTime.minute),
        ]

        with open('Session UT {}.csv'.format(name), 'a', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(dict)
            f.close()


    if int(localTime.hour) <= 6 or int(localTime.hour) >= 19:
        print('The ISS is cruising through the dark night! Sweet trails!')
    else:
        print("The ISS is riding across the bright sky! It's always sunny up there!")
