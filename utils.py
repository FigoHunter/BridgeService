import uuid
from functools import wraps


PORT = 42443
TIMEOUT = 5


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
