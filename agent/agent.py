from abc import *
from enum import Enum
import agent.interaction.message_lib as message_lib

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
        pass
    
    @abstractmethod
    def on_stop(self):
        pass

    @abstractmethod
    def on_subscribe(self, sender:str, message:str):
        return message_lib.MessagePermission.DENIED 

    @abstractmethod
    def on_unsubscribe(self, sender:str, message:str):
        pass 

    @abstractmethod
    def on_request(self, sender:str, message:str):
        return message_lib.MessagePermission.DENIED

    @abstractmethod
    def on_response(self, sender:str, message:str):
        pass

    def publish(self, message:str):
        pass

    def request(self, receiver:str, message:str):
        pass
