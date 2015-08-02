import os
import shippo_status_bot
import unittest
import tempfile
from flask import Flask, request

from webhook.validator import is_valid_error

app = Flask(__name__)


class ValidatorTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, shippo_status_bot.app.config['DATABASE'] = tempfile.mkstemp()
        shippo_status_bot.app.config['TESTING'] = True
        self.app = shippo_status_bot.app.test_client()
        shippo_status_bot.init_db()

    def test_is_valid_error(self):
        with app.test_client() as c:
            rv = c.post('/runscope_webhook')
            is_valid_error(request.get_json())

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(shippo_status_bot.app.config['DATABASE'])

if __name__ == '__main__':
    unittest.main()