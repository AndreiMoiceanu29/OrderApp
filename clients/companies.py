import grpc
from pb_grpc.companies_pb2 import Company
from pb_grpc.companies_pb2 import CreateCompanyRequest, CreateCompanyResponse
from pb_grpc.companies_pb2 import GetCompaniesRequest, GetCompaniesResponse
from pb_grpc.companies_pb2 import UpdateCompanyRequest, UpdateCompanyResponse
from pb_grpc.companies_pb2 import DeleteCompanyRequest, DeleteCompanyResponse
from pb_grpc.companies_pb2_grpc import CompaniesServiceStub

COMPANIES_ENDPOINT = "localhost:50055"

def create_company(company: Company) -> Company:
    with grpc.insecure_channel(COMPANIES_ENDPOINT) as channel:
        stub = CompaniesServiceStub(channel)
        request = CreateCompanyRequest(name=company.name,owner_name=company.owner_name)
        response = stub.CreateCompany(request)
        return response.result
    
def get_companies() -> Company:
    with grpc.insecure_channel(COMPANIES_ENDPOINT) as channel:
        stub = CompaniesServiceStub(channel)
        request = GetCompaniesRequest()
        response = stub.GetCompanies(request)
        return response.results
    
def update_company(old_company_id: str, company: Company) -> Company:
    with grpc.insecure_channel(COMPANIES_ENDPOINT) as channel:
        stub = CompaniesServiceStub(channel)
        request = UpdateCompanyRequest(old_company_id=old_company_id, new_company=company)
        response = stub.UpdateCompany(request)
        return response.result
    
def delete_company(company_id: str) -> Company:
    with grpc.insecure_channel(COMPANIES_ENDPOINT) as channel:
        stub = CompaniesServiceStub(channel)
        request = DeleteCompanyRequest(id=company_id)
        response = stub.DeleteCompany(request)
        return response.result