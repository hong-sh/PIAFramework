from abc import *
from enum import Enum
from time import time_ns
from threading import Lock
from agent.blackboard_cli import BlackBoardClient

class AgentStatus(Enum):
    CREATED = 0
    RUNNING = 1
    STOP = 2
    DESTROYED = 3
    FAIL = 4

class BaseAgent(metaclass=ABCMeta):
    def __init__(self, blackboard_url:str, agent_uri:str):
        self.blackboard_url = blackboard_url
        self.agent_uri = agent_uri
        self.agent_status = AgentStatus.CREATED
        self.on_start()

    def __del__(self):
        self.agent_status = AgentStatus.DESTROYED

    @abstractmethod
    def on_start(self):
        callbacks = {
            "on_subscribe" : self.on_subscribe, 
            "on_unsubscribe" : self.on_unsubscribe,
            "on_request" : self.on_request,
            "on_response" : self.on_response
            }
        self.blackboard_cli = BlackBoardClient(self.agent_uri, self.blackboard_url, callbacks)
        self.response_lock = Lock()
        self.response_buffer = {}
        self.agent_status = AgentStatus.RUNNING

    @abstractmethod
    def on_stop(self):
        # TODO implements stop process
        self.agent_status = AgentStatus.STOP
        pass

    @abstractmethod
    def on_subscribe(self, subscriber:str, key:str):
        pass

    @abstractmethod
    def on_unsubscribe(self, unsubscriber:str, key:str):
        pass

    @abstractmethod
    def on_request(self, requester:str, message_id:str, task:dict):
        pass

    def on_response(self, responser:str, message_id:str, result:dict):
        self.lock.acquire()
        self.response_buffer[message_id] = result
        self.lock.release()

    def wait_for_response(self, message_id:str):
        while True:
            self.lock.acquire()
            if message_id in self.response_buffer:
                result = self.response_buffer[message_id]
                break
        self.lock.release()
        return result

    def subscribe(self, publisher:str, is_pattern:bool, key:str, callback:object):
        self.blackboard_cli.req_subscribe(publisher, is_pattern, key, callback)

    def publish(self, key:str, value:dict):
        self.blackboard_cli.req_publish(key, value)

    def request(self, receiver:str, task:dict):
        message_id = str(time_ns())
        self.blackboard_cli.req_request(receiver, message_id, task)
        return self.wait_for_response(message_id)

    