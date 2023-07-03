import grpc
from pb_grpc.products_pb2 import Product
from pb_grpc.products_pb2 import CreateProductRequest, CreateProductResponse
from pb_grpc.products_pb2 import GetProductsRequest, GetProductsResponse
from pb_grpc.products_pb2 import UpdateProductRequest, UpdateProductResponse
from pb_grpc.products_pb2 import DeleteProductRequest, DeleteProductResponse
from pb_grpc.products_pb2_grpc import ProductsServiceStub

PRODUCTS_ENDPOINT = "localhost:50056"

def create_product(product: Product) -> Product:
    with grpc.insecure_channel(PRODUCTS_ENDPOINT) as channel:
        stub = ProductsServiceStub(channel)
        request = CreateProductRequest(name=product.name,price=product.price)
        response = stub.CreateProduct(request)
        return response.product
    
def get_products() -> Product:
    with grpc.insecure_channel(PRODUCTS_ENDPOINT) as channel:
        stub = ProductsServiceStub(channel)
        request = GetProductsRequest()
        response = stub.GetProducts(request)
        return response.products
    
def get_product_by_id(product_id: str) -> Product:
    with grpc.insecure_channel(PRODUCTS_ENDPOINT) as channel:
        stub = ProductsServiceStub(channel)
        filter_product = Product(id=product_id)
        request = GetProductsRequest(filter_product=filter_product)
        response = stub.GetProducts(request)
        return response.products
    
def update_product(old_product_id: str, product: Product) -> Product:
    with grpc.insecure_channel(PRODUCTS_ENDPOINT) as channel:
        stub = ProductsServiceStub(channel)
        request = UpdateProductRequest(old_product_id = old_product_id,new_product=product)
        response = stub.UpdateProduct(request)
        return response.product
    
def delete_product(product_id: str) -> Product:
    with grpc.insecure_channel(PRODUCTS_ENDPOINT) as channel:
        stub = ProductsServiceStub(channel)
        request = DeleteProductRequest(id=product_id)
        response = stub.DeleteProduct(request)
        return response.product