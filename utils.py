import uuid
from functools import wraps
from figo_common import environ

PORT = 42443
TIMEOUT = 5
VAR_ADDR = 'BRIDGE_SERVICE_ADDR'
VAR_PORT = 'BRIDGE_SERVICE_PORT'

class BridgeAction(dict):
    def __init__(self, from_id, to_id, action, args):
        id = uuid.uuid4().hex.replace('-', '')
        super().__init__(id=id, from_id=from_id, to_id=to_id, action=action, args=args)
        
    @property
    def id(self) -> str:
        return self['id']
    
    @property
    def from_id(self) -> str:
        return self['from_id']
    
    @property
    def to_id(self) -> str:
        return self['to_id']
    
    @property
    def action(self) -> str:
        return self['action']
    
    @property
    def args(self) -> list:
        return self['args']

def set_env_var(addr=None, port=None):
    if addr is not None:
        environ.setEnvVar(VAR_ADDR, addr)
    if port is not None:
        environ.setEnvVar(VAR_PORT, port)

def get_env_var():
    return environ.getEnvVar(VAR_ADDR, None), environ.getEnvVar(VAR_PORT, None)