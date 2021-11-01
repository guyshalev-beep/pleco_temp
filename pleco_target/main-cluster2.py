import grpc

from pleco_target_pb2 import K8sGWRequest
from pleco_target_pb2_grpc import K8sGWStub


if __name__ == '__main__':
    print('start')

    channel = grpc.insecure_channel("34.105.178.3:50051")  # GCP CENTRAL EXTERNAL IP
#GCP
    to = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImQwWjBUSE1pQmFpVTNUZTk3N2YwVzBIZzhzTW1NT2RQbU5rRndTOHdUcVkifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4tc2R6bGMiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjE5NzgyMDEzLWUwZmQtNDgwZi04ZTc4LThkYmYyMTc0Yjc2YSIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.cQ4HyEz-U_IcKn8Tk1Ypauhs8X5pUCJHrSUVf91VJlMH3HEE4kGx1BGTHGIjty5ly7SSeudHgTzvXmnvLgioKu0K1c1fzNYP_h1Xx41EzyXJZLZGRfFeP1YMDc6lzFv0xEqqCJgn6HplKi9gdm0LD4mY9Szvn5vz9cUf3hENfn9QIHWITYWk1_yc1JLqBf3vFq8MyKb5XyYuFL7AIyAq9POoOuKJjIkqaarGpZHDJCrxBOQRR-UQEGVgQHcC-QYfrN972kHRcxTQ40iR8HTOveKPLBKovTGqGZBP7ZKD2iQI8WEEDDqEE8j8ziC7nMKm2io6SvjkF8Xt2e26_Xbbdg"

#GCP
    ho = "34.105.149.127"

    po = "443"
    client = K8sGWStub(channel)

    print("Test")
    ret = client.TestConnection(K8sGWRequest())
    print (ret)

    print("Get NS")
    ret = client.GetNSs(K8sGWRequest(config_file="config_dir/config-gcp2", client_host=ho, client_port=po, client_token=to))
    print (ret)

    print ("create yelb")

    deploymentRes = client.ApplyDeployment(K8sGWRequest(fileName="yaml/redis-server-deployment.yaml", namespace="yelb", client_host=ho, client_port=po, client_token=to))
    print(deploymentRes)
    serviceRes = client.ApplyService(K8sGWRequest(fileName="yaml/redis-server-service.yaml", namespace="yelb", client_host=ho, client_port=po, client_token=to))
    print (serviceRes)

    deploymentRes = client.ApplyDeployment(K8sGWRequest(fileName="yaml/yelb-appserver-deployment.yaml", namespace="yelb", client_host=ho, client_port=po, client_token=to))
    print(deploymentRes)
    serviceRes = client.ApplyService(K8sGWRequest(fileName="yaml/yelb-appserver-service.yaml", namespace="yelb", client_host=ho, client_port=po, client_token=to))
    print (serviceRes)

    deploymentRes = client.ApplyDeployment(K8sGWRequest(fileName="yaml/yelb-db-deployment.yaml", namespace="yelb", client_host=ho, client_port=po, client_token=to))
    print(deploymentRes)
    serviceRes = client.ApplyService(K8sGWRequest(fileName="yaml/yelb-db-service.yaml", namespace="yelb", client_host=ho, client_port=po, client_token=to))
    print (serviceRes)

    deploymentRes = client.ApplyDeployment(K8sGWRequest(fileName="yaml/yelb-ui-deployment.yaml", namespace="yelb", client_host=ho, client_port=po, client_token=to))
    print(deploymentRes)
    serviceRes = client.ApplyService(K8sGWRequest(fileName="yaml/yelb-ui-service.yaml", namespace="yelb", client_host=ho, client_port=po, client_token=to))
    print (serviceRes)



    """
"""
    




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
