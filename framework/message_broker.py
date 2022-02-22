import messaging_service.PIA_message_pb2_grpc as PIA_message_grpc
import messaging_service.PIA_message_pb2 as PIA_message
import blackboard

class MessageBroker(PIA_message_grpc.PIAMessageServiceServicer):
    def __init__(self, broker_url:str, blackboard:blackboard):
        pass