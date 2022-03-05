import redis
from threading import Thread

'''
Message Protocol
publish message : agent-uri/publish/key, value
subscribe(unsubscribe) message : subscribe(unsubscribe)/agent-uri/publisher-uri, key
request message : request/agent-uri/receiver-uri/message_id, value
response message : response/agent-uri/receiver-uri/message_id, value

'''

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
            self.on_noti_thread = Thread(target=self.on_notify()).start()
        except Exception as e:
            print('redis connect error occurred : ', e)

    def initialize_topic(self):
        self.subscribe.psubscribe("subscribe/*/" + self.agent_uri + "/*")
        self.subscribe.psubscribe("unsubscribe/*/" + self.agent_uri + "/*")
        self.subscribe.psubscribe("request/*/" + self.agent_uri + "/*")
        self.subscribe.psubscribe("response/*/" + self.agent_uri + "/*")

    def set_callback(self, key:str, callback:object):
        self.callbacks[key] = callback

    def on_notify(self):
        while True:
            message = self.subscribe.get_message()
            if message['type'] == 'message' or message['type'] == 'pmessage':
                splitted_channel = message['channel'].split("/")
                message_type = splitted_channel[0]
                if splitted_channel[1] in self.callbacks: 
                    if message_type == "subscribe":
                        pass
                    elif message_type == "unsubscribe":
                        pass
                    elif message_type == "request":
                        pass
                    elif message_type == "response":
                        pass

    def req_publish(self, key:str, value:dict):
        pub_key = self.agent_uri + '/publish/' + key
        self.redis_cli.publish(pub_key, value)
        pass

    def req_subscribe(self, publisher:str, is_pattern:bool, key:str, callback:object):
        publish_key = self.agent_uri + "/subscribe/" + publisher + 
        subscribe_key = publisher + "/publish/" + key
        if is_pattern:
            self.subscribe.psubscribe(subscribe_key)
        else:
            self.subscribe.subscribe(subscribe_key)
        self.redis_cli.publish()

    def req_unsubscribe(self, publisher:str, is_pattern:bool, key:str):
        unubscribe_key = publisher + "/unsubscribe/" + key
        if is_pattern:
            self.subscribe.punsubscribe(unubscribe_key)
        else:
            self.subscribe.unsubscribe(unubscribe_key)

    def req_request(self, receiver:str, key:str, value:dict):
        req_key = receiver + '/request/' + self.agent_uri + '/' + key
        self.redis_cli.publish(req_key, value)

    def req_response(self, receiver:str, key:str, value:dict):
        res_key = receiver + '/response/' + self.agent_uri + '/' + key
        self.redis_cli.publish(res_key, value)