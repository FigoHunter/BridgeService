from .flask import *
import logging
from . import utils

def run(port=utils.PORT):
    utils.PORT = port
    logging.basicConfig(filename='app.log', level=log_level)
    app.run(debug=utils.DEBUG, port=port)
    app.logger.info('=============================== Bridge Service Started ===============================')