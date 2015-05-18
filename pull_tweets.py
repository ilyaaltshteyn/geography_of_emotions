#

from config import *
from TwitterAPI import TwitterAPI
import time
import ast

delay = 8 # seconds
dir = "/Users/ilya/Projects/geography_of_emotions/"
with open(dir + 'api_keys.txt') as k:
    keys = ast.literal_eval(k.readlines()[0])

consumer_key = keys['c_k']
consumer_secret = keys['c_s']
access_token_key = keys['a_k']
access_token_secret = keys['a_s']

file_location = "/Users/ilya/Projects/geography_of_emotions/lonely_tweets.txt"

while True:
    try:
        api = TwitterAPI(consumer_key, consumer_secret,
                         access_token_key, access_token_secret)
        r = api.request('statuses/filter', {'track':'lonely'})
        with open(file_location, "a") as output:
            for item in r.get_iterator():
                output.write(str(item) + "\n")
                delay = max(8, delay/2)
    except Exception, e:
        print e
        print "Error"
        print time.ctime()
        print "Waiting " + str(delay) + " seconds"
        time.sleep(delay)
        delay *= 2