import requests
import threading
import time
import traceback
from . import utils

class BridgeServiceClient:
    def __init__(self, name, address='127.0.0.1', port=utils.PORT):
        self.name = name
        self.address = address
        self.port = port
        self._action_registry = {}
        utils.PORT = port
        self._thread = threading.Thread(target=self._heartbeat, daemon=True)
        self._thread.start()
        
    def _heartbeat(self):
        while True:
            try:
                response = requests.post(f'http://{self.address}:{self.port}/bridge-service/retrieve', json={'to_id': self.name},timeout=utils.TIMEOUT)
                if response.status_code != 200:
                    raise Exception(f'Failed to retrieve actions for {self.name}')
                self._parse_response(response)
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                time.sleep(5)
            time.sleep(0.1)

    def _parse_response(self,response:requests.Response):
        for result in response.json():
            try:
                action = result.get('action','')
                args = result.get('args',[])
                if action in self._action_registry:
                    self._action_registry[action](*args)
                else:
                    raise Exception(f'No action found for {action}')
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)

    def send_action(self,to_client,action,args=[]):
        response = requests.post(f'http://{self.address}:{self.port}/bridge-service/register', json={'to_id':to_client,'from_id': self.name, 'action': action, 'args': args},timeout=utils.TIMEOUT)
        if response.status_code != 200:
            raise Exception(f'Failed to send action {action} with args {args}')

    def action(self, key=None):
        def decorator(func):
            nonlocal key
            if key is None:
                key = func.__name__
            self._action_registry[key] = func
            return func
        return decorator


