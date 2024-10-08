from flask import Flask, jsonify
from flask_cors import CORS
import logging
from .. import utils
from .. import core
from flask import request

app = Flask('Bridge Service')
CORS(app)  # Enable CORS for all routes

if utils.DEBUG:
    log_level = logging.DEBUG
else:
    log_level = logging.INFO

def _format_response(success=True, message='', data=None):
    return jsonify(
        {
            'success': success,
            'message': message,
            'data': data
        }
    )

@app.route('/')
def hello():
    app.logger.info('Hello route was accessed')
    return 'Hello, World!'

@app.route('/bridge-service/register', methods=['POST'])
def register():
    from_id = request.json.get('from_id')
    to_id = request.json.get('to_id')
    action = request.json.get('action')
    args = request.json.get('args')
    core.BridgeService.instance().register(from_id, to_id, action, args)
    app.logger.info(f'{from_id} registered action {action} for {to_id}')
    return _format_response(success=True, message='Registered')

@app.route('/bridge-service/retrieve', methods=['POST'])
def retrieve():
    to_id = request.json.get('to_id')
    actions = core.BridgeService.instance().pop_actions(to_id)
    app.logger.info(f'{to_id} retrieved {len(actions)} actions')
    return _format_response(success=True, message='Retrieved', data=actions)

@app.route('/bridge-service/clear', methods=['POST'])
def clear():
    to_id = request.json.get('to_id')
    actions = core.BridgeService.instance().pop_actions(to_id)
    return _format_response(success=True, message='Cleared', data=actions)