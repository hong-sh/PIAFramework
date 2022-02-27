import redis
from threading import Thread

class AgentMessage:

class BlackBoardClient:
    def __init__(self, agent_uri:str, blackboard_url:str, callbacks:object):
        try:
            self.agent_uri = agent_uri
            self.callbacks = callbacks
            splitted_url = blackboard_url.split(":")
            host, port = splitted_url[0], splitted_url[1]
            self.redis_cli = redis.Redis(host=host, port=port, db=0)
            self.subscribe = self.redis_cli.pubsub()
            self.initialize_topic()
            self.on_sub_thread = Thread(target=self.on_subscribe())
            self.on_sub_thread.start()
        except Exception as e:
            print('redis connect error occurred : ', e)

    def initialize_topic(self):
        self.subscribe.psubscribe(self.agent_uri)

    def on_subscribe(self):
        while True:
            message = self.subscribe.get_message()
            self.subscribe.

    def req_publish(self, key:str, value:dict):
        pub_key = self.agent_uri + '/publish/' + key
        self.redis_cli.publish(pub_key, value)
        pass

    def req_subscribe(self, subscriber:str, receiver:str, subscribe_pattern:str):
        self.redis_cli.pubsub()
        pass

    def req_unsubscribe(self, subscirber:str, receiver:str, unsubscribe_pattern:str):
        self.redis_cli.pubsub()
        pass