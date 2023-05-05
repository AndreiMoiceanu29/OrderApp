import grpc
from pb_grpc.drone_manager_pb2_grpc import DroneManagerStub
from pb_grpc.drone_manager_pb2 import SetGoalRequest, SetGoalResponse
from pb_grpc.drone_manager_pb2 import LandDroneResponse
from google.protobuf.empty_pb2 import Empty

class DroneManagerClient:

    def __init__(self, host: str, port: str) -> None:
        self.host = host
        self.port = port

    def set_goal(self, x: float, y: float, z: float) -> str:
        with grpc.insecure_channel(f"{self.host}:{self.port}") as channel:
            stub = DroneManagerStub(channel)
            request = SetGoalRequest(x=x,y=y,z=z)
            response = stub.SetGoal(request)
            return response.order_id
        
    def land_drone(self) -> str:
        with grpc.insecure_channel(f"{self.host}:{self.port}") as channel:
            stub = DroneManagerStub(channel)
            request = Empty()
            response = stub.LandDrone(request)
            return response.success
        
    
        
