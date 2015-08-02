import datetime
import os
from enum import Enum
import tweepy, time, sys


#enter the corresponding information from your Twitter application:
CONSUMER_KEY = os.getenv('CONSUMER_KEY')  #keep the quotes, replace this with your consumer key
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET') #keep the quotes, replace this with your consumer secret key
ACCESS_KEY = os.getenv('ACCESS_KEY') #keep the quotes, replace this with your access token
ACCESS_SECRET = os.getenv('ACCESS_SECRET') #keep the quotes, replace this with your access token secret
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

carriers = {
    'Endicia Label Purchase': 'Endicia',
    'Endicia Label Purchase Copy (testing for hackathon)': 'Endicia',
    'FedEx (Production Endpoint)': 'FedEx Shipping',
    'Parcel2Go Test': 'Parcel2Go Shipping',
    'Mondial Relay Test': 'Mondial Relay Shipping',
    'UPS International Return Label': 'UPS Shipping'
}


def post_to_twitter(json):
    adapter_name = carriers[json['test_name']]
    time_fmt = datetime.datetime.now().strftime('%d %b %Y - %I:%M %p')
    api.update_status(status='%s API is down as of %s' % (adapter_name, time_fmt))

def post_to_twitter_back_up(json):
    adapter_name = carriers[json['test_name']]
    time_fmt = datetime.datetime.now().strftime('%d %b %Y - %I:%M %p')
    api.update_status(status='%s API is back up as of %s' % (adapter_name, time_fmt))
