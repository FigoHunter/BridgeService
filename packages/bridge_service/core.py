from queue import Queue
import copy
import threading
from bridge_service_client.utils import BridgeAction


class BridgeService:
    @classmethod
    def instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self._thread = None
        self._registered = {}
        self._actions={}
        self._action_lock = threading.RLock()

    def register(self, from_id, to_id, action, args = []):
        action = BridgeAction(from_id, to_id, action, args)
        self._add_action(action)

    def pop_actions(self, to_id):
        actions = self._pop_actions(to_id)
        return actions
    
    def _get_action(self, id):
        return self._actions.get(id)

    def _add_action(self, action):
        self._action_lock.acquire()
        self._actions[action.id] = action
        actions = self._registered.get(action.to_id, [])
        if id not in actions:
            actions.append(action.id)
        self._registered[action.to_id] = actions
        self._action_lock.release()

    def _remove_action(self, id):
        self._action_lock.acquire()
        action = self._actions.pop(id)
        actions = self._registered.get(action.to_id, [])
        if id in actions:
            actions.remove(id)
        self._registered[action.to_id] = actions
        self._action_lock.release()
        
    def _pop_actions(self, to_id):
        self._action_lock.acquire()
        actions = copy.copy(self._registered.get(to_id, []))
        if to_id in self._registered:
            del self._registered[to_id]
        result = []
        for id in actions:
            bsaction = self._actions.pop(id)
            result.append(bsaction)
        self._action_lock.release()
        return result


    # def run(self):
    #     self._thread = threading.Thread(target=self._run, daemon=True)
    #     self._thread.start()

    # def _run(self):
    #     raise NotImplementedError

    # def stop(self):
    #     raise NotImplementedError
