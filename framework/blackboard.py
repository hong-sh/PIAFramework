import redis

class BlackBoard:
    def __init__(self, blackboard_url:str):
        try:
            splitted_url = blackboard_url.split(":")
            host, port = splitted_url[0], splitted_url[1]
            self.redis_cli = redis.Redis(host=host, port=port, db=0)
            self.subscribe = self.redis_cli.pubsub()
        except Exception as e:
            print('redis connect error occurred : ', e)

    def req_publish(self, publisher:str, message:str):
        
        self.redis_cli.publish()

    def req_subscribe(self, subscriber:str, receiver:str, message:str):
        pass