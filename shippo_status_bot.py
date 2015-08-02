import os
from flask import Flask, request
import logging

from webhook.validator import is_valid_error, is_error, check_status, change_status_to_up, change_status_to_down
from webhook.twitter import post_to_twitter, post_to_twitter_back_up

# http://stackoverflow.com/questions/20457567/flask-logging-with-foreman
from logging import StreamHandler
file_handler = StreamHandler()
app = Flask(__name__)

app.logger.addHandler(file_handler)
app.logger.setLevel(logging.DEBUG)  # set the desired logging level here


@app.route('/')
def hello():
    return 'Hello World!'


@app.route('/runscope_webhook', methods=['POST'])
def runscope_webhook():
    app.logger.info('Received webhook: %s' % str(request.get_json()))
    valid = is_valid_error(request.get_json())
    if valid:
        # post that the api is down
        change_status_to_down(request.get_json())
        post_to_twitter(request.get_json())
    elif not is_error(request.get_json()):
        app.logger.info('test is passing, now checking if we have it set as down and need to set it as up')
        # check if we need to update the 'down' status to 'up'
        if not check_status(request.get_json()):
            # the status is down
            app.logger.info('the status is down and we need to set it as up')
            change_status_to_up(request.get_json())
            post_to_twitter_back_up(request.get_json())

    return 'SUCCESS'
