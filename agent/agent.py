from abc import *
from enum import Enum
from agent.blackboard_cli import BlackBoardClient

class AgentStatus(Enum):
    CREATED = 0
    RUNNING = 1
    DESTROYED = 2
    FAIL = 3

class BaseAgent(metaclass=ABCMeta):
    def __init__(self, blackboard_url:str, agent_uri:str):
        self.blackboard_url = blackboard_url
        self.agent_uri = agent_uri
        self.agent_status = AgentStatus.CREATED

    @abstractmethod
    def on_start(self):
        callbacks = {
            "on_subscribe" : self.on_subscribe, 
            "on_unsubscribe" : self.on_unsubscribe,
            "on_request" : self.on_request,
            "on_response" : self.on_response
            }
        self.blackboard_cli = BlackBoardClient(self.agent_uri, self.blackboard_url, callbacks)
    
    @abstractmethod
    def on_stop(self):
        pass

    @abstractmethod
    def on_subscribe(self, requester:str, key:str):
        pass

    @abstractmethod
    def on_unsubscribe(self, :str, message:str):
        pass

    def on_notify(self, publisher:str, key:str, value:dict):
        pass

    @abstractmethod
    def on_request(self, sender:str, message:str):
        pass

    @abstractmethod
    def on_response(self, sender:str, message:str):
        pass

    def publish(self, message:str):
        pass

    def request(self, receiver:str, message:str):
        pass
