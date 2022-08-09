from urllib.request import urlopen
import json
from datetime import *
import pytz
from tzwhere import tzwhere
from timezonefinder import TimezoneFinder
import tweepy

clientID = "***"
clientSecret = "***"
APIkey = "***"
APIsecret = "***"
BToken = "***"
accessToken = "***"
accessTokenSecret = "***"

auth = tweepy.OAuthHandler(APIkey, APIsecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)

#doLog = input('Log session? (y/n) \n')

initReq = urlopen("http://api.open-notify.org/iss-now.json").read()
initObj = json.loads(initReq)

name = initObj['timestamp']

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
if int(localTime.hour) <= 6 or int(localTime.hour) >= 19:
    phrase = 'The ISS is cruising through the dark night! Currently flying over {} region ({}, {}) \nSweet Trails!'.format(timezoneISS, latt, long)
else:
    phrase = "The ISS is slicing through the bright, blue sky! Currently flying over {} region ({}, {}) \nHappy days!".format(timezoneISS, latt, long)

api.update_status(status = phrase)
print(phrase)
phrase = ''
