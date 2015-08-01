import os
from flask import Flask, request

app = Flask(__name__)

# http://stackoverflow.com/questions/20457567/flask-logging-with-foreman
import logging
from logging import StreamHandler
file_handler = StreamHandler()
app.logger.setLevel(logging.DEBUG)  # set the desired logging level here
app.logger.addHandler(file_handler)

@app.route('/')
def hello():
    return 'Hello World!'


@app.route('/runscope_webhook', methods=['POST'])
def runscope_webhook():
    app.logger.info('Received webhook: %s' % str(request.get_json()))
    return 'SUCCESS'
