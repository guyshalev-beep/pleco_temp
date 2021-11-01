import time

import grpc

from pleco_target_pb2 import K8sGWRequest
from pleco_target_pb2_grpc import K8sGWStub


def createService(*resource_names, client, api_server, token):
    for resource_name in resource_names:
        print("start deploy service %s" % resource_name)
        service_res = client.ApplyService(
            K8sGWRequest(fileName="yaml/services/%s-svc.yaml" % resource_name, namespace="online-boutique",
                         client_host=api_server,
                         client_port=po,
                         client_token=token))
        print(service_res)


def createResource(*resource_names, client, api_server, token):
    for resource_name in resource_names:
        print("start deploy %s" % resource_name)
        deployment_res = client.ApplyDeployment(
            K8sGWRequest(fileName="yaml/deployments/%s-deployment.yaml" % resource_name, namespace="online-boutique",
                         client_host=api_server, client_port=po,
                         client_token=token))
        print(deployment_res)
        service_res = client.ApplyService(
            K8sGWRequest(fileName="yaml/services/%s-svc.yaml" % resource_name, namespace="online-boutique",
                         client_host=api_server,
                         client_port=po,
                         client_token=token))
        print(service_res)


def deleteResource(*resource_names, client, api_server, token):
    for resource_name in resource_names:
        print("start delete %s" % resource_name)
        deploymentRes = client.DeleteDeployment(
            K8sGWRequest(resourceName=resource_name, namespace="online-boutique", client_host=api_server,
                         client_port=po,
                         client_token=token))
        print(deploymentRes)
  #      serviceRes = client.DeleteService(
  #          K8sGWRequest(resourceName=resource_name, namespace="online-boutique", client_host=api_server,
  #                       client_port=po,
  #                       client_token=token))
  #      print(serviceRes)


def leapResource(*resource_names, client_founder, client_co_founder, api_server_founder, api_server_co_founder,
                 token_founder, token_co_founder):
    for resource_name in resource_names:
        print("apply %s on co-founder" % resource_name)
        createResource(resource_name, client=client_co_founder, api_server=api_server_co_founder,
                       token=token_co_founder)
        time.sleep(10)
        print("remove %s from founder" % resource_name)
        deleteResource(resource_name, client=client_founder, api_server=api_server_founder, token=token_founder)


if __name__ == '__main__':
    print('start')
    channel_founder = grpc.insecure_channel("34.105.149.16:50051")  # GCP moon external-ip
    channel_co_founder = grpc.insecure_channel("34.102.16.134:50051")  # GCP moon-co external-ip
    token_founder = "eyJhbGciOiJSUzI1NiIsImtpZCI6Ii1VSUE5UkcyY3pNeWRYc0dOWEJicjFlRkQwUTFPUXRVUVhsRkRONW5YSWcifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4tNXc0ZnYiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6ImYyOTQ5OWMwLTYxNWYtNDQ0YS05ZGVkLTg4ZGRiYWNjNzQwNyIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.gFuk3Q_J4dWiX680HREtxXFR5gNJix8AqFcAK_vWljrT0Ixratrr4m_s2z91oT-UBMqFPes8Bx6EyfmqNmWKewuT2JMaTh9H6dAhgkWtUQ7h36a_CzrRkhgxnGsiIzUaB83tMXnfL7C254bbsGCKVEeNX1sW-h6jaRh4GwupxlfEaa-TByCUPGuc4CxR5t1HjDrygZAOMB3JVoU7Sel4wfBeWMEA-Ebx2n-TqMF_rwiRDqF_pA_OtcjGBQnodmF-xYD0zUe1R21OPAi2jHOmQOH5UJpXIN4EU0w523z3hdKYKwjumPJR5aw37zktw6o6TTuGdMBRwbEZr6R8wsV-yg"
    token_co_founder = "eyJhbGciOiJSUzI1NiIsImtpZCI6InVTUmVwN2ZCYVA0TFJnZVVOME9yOUc5bVdGeDBJVjlYMHFjODJTYlI3ZlUifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4teHZsdnMiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjBhZDI4MmEzLTk5ZmUtNDFjYy04ZGFjLWU3YTE0ZGI4MDhkNSIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.FH-rF1JMd9PgfyR_qQssQ7T-zUZtgXOUJEf4KxSyvjhZ61mR47sfdUGJxzWbZB653UKTzow3KfOKSmfPNXsF_Vwrp60ecx0E7L5EYrP0I4G0R3PuIZCumT1PNDACRjNVqBy4Ba6nis9HTwJaD-jPXprNTKu0xx7q4bmwa-Rf2Xw7ug9Lxux6snglZUNm5gNei745J803jXKl3hKLB8Mj1wkcg5Usuv4e3yO7UZ684j0T-wEmS33MIP8ADudIyRwtAd7CJkisXiUy949TmraHsA80eN4E1sA8sCK0ALdFZZ5jtgkPpK69yDgM0ay0vFyysxcwe0k9xcVDe4SUfpQCnw"
    api_server_founder = "34.105.136.235"
    api_server_co_founder = "34.94.50.9"
    po = "443"
    client_founder = K8sGWStub(channel_founder)
    client_co_founder = K8sGWStub(channel_co_founder)

    print("Test Founder")
    ret = client_founder.TestConnection(K8sGWRequest())
    print(ret)
    print("Test Co-Founder")
    ret = client_co_founder.TestConnection(K8sGWRequest())
    print(ret)

    print("Get NS Founder")
    ret = client_founder.GetNSs(
        K8sGWRequest(config_file="config_dir/config-gcp2", client_host=api_server_founder, client_port=po,
                     client_token=token_founder))
    print(ret)
    print("Get NS Co-Founder")
    ret = client_co_founder.GetNSs(
        K8sGWRequest(config_file="config_dir/config-gcp2", client_host=api_server_co_founder, client_port=po,
                     client_token=token_co_founder))
    print(ret)
    # , "checkoutservice" "productcatalogservice"  "cartservice",

    createService("cartservice", "adservice", "checkoutservice", "currencyservice", "emailservice", "frontend",
                  "paymentservice", "productcatalogservice", "recommendationservice", "redis-cart", "shippingservice",
                  client=client_founder, api_server=api_server_founder,
                  token=token_founder)
    createService("cartservice", "adservice", "checkoutservice", "currencyservice", "emailservice", "frontend",
                  "paymentservice", "productcatalogservice", "recommendationservice", "redis-cart", "shippingservice",
                  client=client_co_founder, api_server=api_server_co_founder,
                  token=token_co_founder)
    leapResource("adservice", "checkoutservice", "currencyservice", "emailservice", "paymentservice", "shippingservice",
                 client_founder=client_founder, client_co_founder=client_co_founder,
                 api_server_founder=api_server_founder, api_server_co_founder=api_server_co_founder,
                 token_founder=token_founder, token_co_founder=token_co_founder)