import grpc

from pleco_target_pb2 import K8sGWRequest
from pleco_target_pb2_grpc import K8sGWStub


def createResource(*resource_names):
    for resource_name in resource_names:
        print("start deploy %s" % resource_name)
        deployment_res = client.ApplyDeployment(
            K8sGWRequest(fileName="yaml/deployments/%s-deployment.yaml" % resource_name, namespace="online-boutique",
                         client_host=ho, client_port=po,
                         client_token=to))
        print(deployment_res)
        service_res = client.ApplyService(
            K8sGWRequest(fileName="yaml/services/%s-svc.yaml" % resource_name, namespace="online-boutique", client_host=ho,
                         client_port=po,
                         client_token=to))
        print(service_res)

if __name__ == '__main__':
    print('start')
    channel = grpc.insecure_channel("34.105.149.16:50051")  # GCP moon external-ip
    # GCP
    to = "eyJhbGciOiJSUzI1NiIsImtpZCI6Ii1VSUE5UkcyY3pNeWRYc0dOWEJicjFlRkQwUTFPUXRVUVhsRkRONW5YSWcifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4tNXc0ZnYiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6ImYyOTQ5OWMwLTYxNWYtNDQ0YS05ZGVkLTg4ZGRiYWNjNzQwNyIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.gFuk3Q_J4dWiX680HREtxXFR5gNJix8AqFcAK_vWljrT0Ixratrr4m_s2z91oT-UBMqFPes8Bx6EyfmqNmWKewuT2JMaTh9H6dAhgkWtUQ7h36a_CzrRkhgxnGsiIzUaB83tMXnfL7C254bbsGCKVEeNX1sW-h6jaRh4GwupxlfEaa-TByCUPGuc4CxR5t1HjDrygZAOMB3JVoU7Sel4wfBeWMEA-Ebx2n-TqMF_rwiRDqF_pA_OtcjGBQnodmF-xYD0zUe1R21OPAi2jHOmQOH5UJpXIN4EU0w523z3hdKYKwjumPJR5aw37zktw6o6TTuGdMBRwbEZr6R8wsV-yg"
    # GCP moon api server
    ho = "34.105.136.235"
    po = "443"
    client = K8sGWStub(channel)
    print("Test")
    ret = client.TestConnection(K8sGWRequest())
    print(ret)
    print("Get NS")
    ret = client.GetNSs(
        K8sGWRequest(config_file="config_dir/config-gcp2", client_host=ho, client_port=po, client_token=to))
    print(ret)
    print("create online-boutique")
    createResource("cartservice","adservice","checkoutservice","currencyservice","emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "redis-cart", "shippingservice")


