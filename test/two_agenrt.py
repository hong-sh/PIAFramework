from framework import PIAframework
from agent.PIAagent import BaseAgent

class AgentAlpha(BaseAgent):
    def __init__(self, blackboard_url, agent_uri):
        super().__init__(blackboard_url, agent_uri)

    def on_subscribe(self, subscriber: str, key: str):
        return super().on_subscribe(subscriber, key)

    def on_unsubscribe(self, unsubscriber: str, key: str):
        return super().on_unsubscribe(unsubscriber, key)

    def on_request(self, requester: str, message_id: str, task: dict):
        return super().on_request(requester, message_id, task)


class AgentBeta(BaseAgent):
    def __init__(self, blackboard_url, agent_uri):
        super().__init__(blackboard_url, agent_uri)

    def on_subscribe(self, subscriber: str, key: str):
        return super().on_subscribe(subscriber, key)

    def on_unsubscribe(self, unsubscriber: str, key: str):
        return super().on_unsubscribe(unsubscriber, key)

    def on_request(self, requester: str, message_id: str, task: dict):
        return super().on_request(requester, message_id, task)


if __name__ == "__main__":
    PIAframework.run()
    alpha = AgentAlpha("127.0.0.1:6379", "alpha")
    beta = AgentBeta("127.0.0.1:6379", "beta")