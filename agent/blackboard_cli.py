import redis
from threading import Thread

'''
Message Protocol
publish message : publish/agent-uri/key, value
subscribe(unsubscribe) message : subscribe(unsubscribe)/agent-uri/publisher-uri, key
request message : request/agent-uri/receiver-uri/message_id, task
response message : response/agent-uri/receiver-uri/message_id, result
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

    def on_notify(self):
        while True:
            message = self.subscribe.get_message()
            if message['type'] == 'message' or message['type'] == 'pmessage':
                splitted_channel = message['channel'].split("/")
                message_type = splitted_channel[0]
                if splitted_channel[1] in self.callbacks: 
                    if message_type == "subscribe":
                        self.callbacks["on_subscribe"](subscriber=splitted_channel[1], key=message['data'])
                    elif message_type == "unsubscribe":
                        self.callbacks["on_unsubscribe"](unsubscriber=splitted_channel[1], key=message['data'])
                    elif message_type == "request":
                        self.callbacks["on_request"](requester=splitted_channel[1], message_id=splitted_channel[3], task=message['data'])
                    elif message_type == "response":
                        self.callbacks["on_response"](responser=splitted_channel[1], message_id=splitted_channel[3], result=message['data'])

    def req_publish(self, key:str, value:dict):
        pub_key = "publish/" + self.agent_uri + "/" + key
        self.redis_cli.publish(pub_key, value)
        pass

    def req_subscribe(self, publisher:str, is_pattern:bool, key:str, callback:object):
        publish_key = "subscribe/" + self.agent_uri + "/" + publisher + "/" + key
        subscribe_key = "publish/" + publisher + "/" + key

        self.redis_cli.publish(publish_key)
        if is_pattern:
            self.subscribe.psubscribe(subscribe_key)
        else:
            self.subscribe.subscribe(subscribe_key)
        self.callbacks[subscribe_key] = callback

    def req_unsubscribe(self, publisher:str, is_pattern:bool, key:str):
        publish_key = "unsubscribe/" + self.agent_uri + "/" + publisher + "/" + key
        unubscribe_key = "publish/" + publisher + "/" + key

        self.redis_cli.publish(publish_key)
        if is_pattern:
            self.subscribe.punsubscribe(unubscribe_key)
        else:
            self.subscribe.unsubscribe(unubscribe_key)
        del self.callbacks[unubscribe_key]

    def req_request(self, receiver:str, message_id:str, task:dict):
        req_key = "request/" + self.agent_uri + "/" + receiver + "/" + message_id
        self.redis_cli.publish(req_key, task)

    def req_response(self, receiver:str, message_id:str, task:dict):
        res_key = "response/" + self.agent_uri + "/" + receiver + "/" + message_id
        self.redis_cli.publish(res_key, task)