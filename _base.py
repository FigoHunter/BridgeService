import requests
import threading
import time
import traceback
from . import utils

class BridgeServiceClient:
    def __init__(self, name, address=None, port=None):
        if address is None:
            address = '127.0.0.1'
        if port is None:
            port = utils.PORT
        self.name = name
        self.address = address
        self.port = port
        self._action_registry = {}
        self._thread = None
        self._stopped = True
        self._wait_lock = threading.Event()
        self._start_wait_lock = threading.Event()
        self._start_wait_lock.set()
        self._request_lock = threading.RLock()
        

    def _heartbeat(self):
        while True:
            if self._stopped:
                break
            self._request_lock.acquire()
            try:
                response = requests.post(f'http://{self.address}:{self.port}/bridge-service/retrieve', json={'to_id': self.name},timeout=utils.TIMEOUT)
                if response.status_code != 200:
                    raise Exception(f'Failed to retrieve actions for {self.name}')
                self._parse_response(response)
                self._start_wait_lock.set()
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                time.sleep(3)
                self._start_wait_lock.set()
            self._request_lock.release()
            time.sleep(0.2)

    def _parse_response(self,response:requests.Response):
        if len(response.json()['data']) == 0:
            return
        for result in response.json()['data']:
            try:
                action = result.get('action','')
                args = result.get('args',[])
                if action in self._action_registry:
                    self._action_registry[action](*args)
                else:
                    raise Exception(f'No action found for {action}')
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
        self._wait_lock.set()

    def connect(self, daemon=True):
        if self._thread is None:
            self._thread = threading.Thread(target=self._heartbeat, daemon=daemon)
            self._stopped = False
            self._thread.start()

    def send_action(self,to_client,action,*args, wait=False, timeout=10):
        if wait and not self._stopped:
            self._wait_lock.clear()
            self._start_wait_lock.clear()
            self._start_wait_lock.wait()
        try:
            self._request_lock.acquire()
            response = requests.post(f'http://{self.address}:{self.port}/bridge-service/register', json={'to_id':to_client,'from_id': self.name, 'action': action, 'args': list(args)},timeout=utils.TIMEOUT)
            if response.status_code != 200:
                raise Exception(f'Failed to send action {action} with args {args}')
            self._request_lock.release()        
        except Exception as e:
            self._request_lock.release()
            raise e
        if wait and not self._stopped:
            self._wait_lock.wait(timeout)


    def action(self, key=None):
        def decorator(func):
            nonlocal key
            if key is None:
                key = func.__name__
            self._action_registry[key] = func
            return func
        return decorator

    def stop(self):
        self._stopped = True

    def send_clear(self):
        response = requests.post(f'http://{self.address}:{self.port}/bridge-service/clear', json={'to_id': self.name},timeout=utils.TIMEOUT)
        if response.status_code != 200:
            raise Exception(f'Failed to clear actions for {self.name}')

