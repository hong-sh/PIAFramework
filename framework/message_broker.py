from concurrent import futures
import messaging_service.PIA_message_pb2_grpc as PIA_message_grpc
import messaging_service.PIA_message_pb2 as PIA_message
import blackboard
import grpc
from threading import Thread

class MessageBroker(PIA_message_grpc.PIAMessageServiceServicer):
    def __init__(self, broker_url:str, blackboard:blackboard):
        self.broker_url = broker_url
        self.black_board = blackboard
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        PIA_message_grpc.add_PIAMessageServiceServicer_to_server(PIAMessageService(self), self.server)
        self.server.add_insecure_port(self.broker_url)
        self.server.start()
        thread = Thread(target=self.server.wait_for_termination())
        thread.start()

    def on_publish(self, message:PIA_message.PublishMessage):
        # TODO unmarshal message
        blackboard.req_publish()
        pass

    def on_subscribe(self, message:PIA_message.SubscribeMessage):
        blackboard.req_subscribe()
        pass

    def on_unsubscribe(self, message:PIA_message.SubscribeMessage):
        blackboard.req_unsubscribe()
        pass

    def on_request(self, message:PIA_message.RequestMessage):
        # TODO interaction directly request
        pass

        
class PIAMessageService(PIA_message_grpc.PIAMessageServiceServicer):
    def __init__(self, message_broker:MessageBroker):
        self.message_broker = message_broker

    def Publish(self, request, context):
        self.message_broker.on_publish(request)
        return super().Publish(request, context)

    def Subscribe(self, request, context):
        self.message_broker.on_subscribe(request)
        return super().Subscribe(request, context)

    def UnSubscribe(self, request, context):
        self.message_broker.on_unsubscribe(request)
        return super().UnSubscribe(request, context)

    def Request(self, request, context):
        self.message_broker.on_request(request)
        return super().Request(request, context)