import logging
import time
from flask import Flask
from twitter import carriers
# http://stackoverflow.com/questions/20457567/flask-logging-with-foreman
from logging import StreamHandler
file_handler = StreamHandler()
app = Flask(__name__)

app.logger.addHandler(file_handler)
app.logger.setLevel(logging.DEBUG)  # set the desired logging level here


CARRIER_STATUS = {
    'Endicia': [True, []]  # True means up, False means down
    'FedEx Shipping': [True, []]  # True means up, False means down
    'Parcel2Go Shipping': [True, []]  # True means up, False means down
    'Mondial Relay Shipping': [True, []]  # True means up, False means down
}

def is_valid_error(json):
    '''Check if the json is a valid error before posting status update (to twitter, email, etc...)'''
    # First check if error
    if is_error(json):
        if check_recent_errors(json):
            # this means that this is the second error we've encountered in 5 minutes
            app.logger.info('json IS valid error')
            return True
        app.logger.info('json IS valid error but it is isolated')
    app.logger.info('json IS NOT valid error')
    return False

def is_error(json):
    if json['result'] != 'pass':
        return True
    return False

def check_recent_errors(json):
    global CARRIER_STATUS  # now we can change it
    if len(CARRIER_STATUS[carriers[json['test_name']]][1]) != 0:
        if (time.time() - CARRIER_STATUS[carriers[json['test_name']]][1][-1]) < 300:
            # there was another error less than 5 minutes ago
            CARRIER_STATUS[carriers[json['test_name']]][1] = []
            return True
    else:
        CARRIER_STATUS[carriers[json['test_name']]][1] = [time.time()]
    return False

def check_status(json):
    if CARRIER_STATUS[carriers[json['test_name']]][0] == True:
        # this carrier is up
        return True
    return False

def change_status_to_up(json):
    global CARRIER_STATUS
    CARRIER_STATUS[carriers[json['test_name']]][0] = True
    CARRIER_STATUS[carriers[json['test_name']]][1] = []

def change_status_to_down(json):
    global CARRIER_STATUS
    CARRIER_STATUS[carriers[json['test_name']]][0] = False
