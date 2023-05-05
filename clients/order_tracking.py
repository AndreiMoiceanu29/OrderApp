import grpc
from pb_grpc.order_tracking_pb2 import Order,Status,Destination
from pb_grpc.order_tracking_pb2_grpc import OrderTrackingServiceStub
from pb_grpc.order_tracking_pb2 import CreateOrderRequest, CreateOrderResponse
from pb_grpc.order_tracking_pb2 import GetOrderRequest, GetOrderResponse
from pb_grpc.order_tracking_pb2 import UpdateOrderRequest, UpdateOrderResponse
from pb_grpc.order_tracking_pb2 import DeleteOrderRequest, DeleteOrderResponse

class OrderTrackingClient:

    def __init__(self, host: str, port: str) -> None:
        self.host = host
        self.port = port

    def get_order_status(self, order_id: str) -> Order:
        with grpc.insecure_channel(f"{self.host}:{self.port}") as channel:
            stub = OrderTrackingServiceStub(channel)
            request = GetOrderRequest(id=order_id)
            response = stub.GetOrder(request)
            return response.order.status
        
    
        
