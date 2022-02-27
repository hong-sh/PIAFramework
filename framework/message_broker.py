from concurrent import futures
import framework.messaging_service.PIA_message_pb2_grpc as PIA_message_grpc
import framework.messaging_service.PIA_message_pb2 as PIA_message
import framework.blackboard
import grpc
from google.protobuf.empty_pb2 import Empty
from threading import Thread

class MessageBroker(PIA_message_grpc.PIAMessageServiceServicer):
    def __init__(self, broker_url:str, blackboard:framework.blackboard):
        self.broker_url = broker_url
        self.blackboard = blackboard
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        PIA_message_grpc.add_PIAMessageServiceServicer_to_server(PIAMessageService(self), self.server)
        self.server.add_insecure_port(self.broker_url)
        self.server.start()
        thread = Thread(target=self.server.wait_for_termination())
        thread.start()

    def on_publish(self, message:PIA_message.PublishMessage):
        message_id = message.message_id
        publisher = message.publisher
        receiver = message.receiver
        publish_key = message.publish_key
        publish_value = message.publish_value
        self.blackboard.req_publish(message_id, publisher, receiver, publish_key, publish_value)

    def on_subscribe(self, message:PIA_message.SubscribeMessage):
        message_id = message.message_id
        subscriber = message.subscriber
        receiver = message.receiver
        subscribe_pattern = message.subscribe_pattern
        result = self.blackboard.req_subscribe(message_id, subscriber, receiver, subscribe_pattern)
        response = PIA_message.ResponseSubscribe()
        response.message_id = result["message_id"]
        response.response_status = result["response_status"]
        response.subscribe_message = message
        return response

    def on_unsubscribe(self, message:PIA_message.SubscribeMessage):
        message_id = message.message_id
        subscriber = message.subscriber
        receiver = message.receiver
        unsubscribe_pattern = message.subscribe_pattern
        result = self.blackboard.req_unsubscribe(message_id, subscriber, receiver, unsubscribe_pattern)
        response = PIA_message.ResponseSubscribe()
        response.message_id = result["message_id"]
        response.response_status = result["response_status"]
        response.subscribe_message = message
        return response

    def on_request(self, message:PIA_message.RequestMessage):
        message_id = message.message_id
        requester = message.requester
        receiver = message.receiver
        request_key = message.request_key
        request_value = message.request_value
        self.blackboard.req_request(message_id, requester, receiver, request_key, request_value)

class PIAMessageService(PIA_message_grpc.PIAMessageServiceServicer):
    def __init__(self, message_broker:MessageBroker):
        self.message_broker = message_broker
        return Empty()

    def Publish(self, request, context):
        self.message_broker.on_publish(request)

    def Subscribe(self, request, context):
        return self.message_broker.on_subscribe(request)

    def UnSubscribe(self, request, context):
        return self.message_broker.on_unsubscribe(request)

    def Request(self, request, context):
        return self.message_broker.on_request(request)
