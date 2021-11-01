import grpc

from pleco_target_pb2 import K8sGWRequest
from pleco_target_pb2_grpc import K8sGWStub


if __name__ == '__main__':
    print('start')

    channel = grpc.insecure_channel("192.168.50.184:50051") #TAL
    channel = grpc.insecure_channel("192.168.50.13:50051") #MAIN
    channel = grpc.insecure_channel("104.197.16.122:50051") #GCP
    channel = grpc.insecure_channel("35.197.231.235:50051")  # GCP CLUSTER1 CLIENT EXTERNAL_IP
    channel = grpc.insecure_channel("192.168.50.184:50051")  # TAL
#TAL
    to = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjNpUVRWdE40TnBFLTlBSlRfNktMbmdQc2NYazFtM3ktLUNIUkR4dWdoM0kifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4tOXJuNXAiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjFiNTVkNzM4LWU2MjQtNDc5Zi1hNTVlLThiZTM2MWI4YzQzMiIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.nyc7Kr-jMdXQXR27Mbf44bOoYi5zVKJ0QqYO06jPj--_OUTEs388B3ylr3tXT79Mxc2P0uFR-_JoJ6fo6XMFKvSHbEkTtFpTfxUTfHSX5_GSGitp2u3SYpfEZ3Hva8Bk_VyD-Zg-c2-0381HbIHloPxh9J0nkjBIgG0rhgijOadDl2E9wWXqWn9ew4-SYaogmqyenweQesSf3iheyGtauP9lhxuJ_GR71IPZ96n27Jq1aiG0Ae-C9xp1Do9abNcNjGCZ2mduVqkSnKNBFRAKAJ-hHzyadqpz1tUoE-0NwwtqnxWF7DrQbFDpYIehY_ccHksqY3FwP1AnhiSGOLPaZQ"
#GCP CLUSTER1
    to = "eyJhbGciOiJSUzI1NiIsImtpZCI6InhGOTRrR3V1N2hSVHF4b0lmRmwyRmJhVmRSdFJRSVRmOU84QWl4M2d3bkEifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4tOGxzaHYiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6ImYxZTgzMDE3LWVjMmMtNDE3OS1iNmQ1LTZiZTdmZTgyYzZkZCIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.jUreoN4i8miN7NtRoOYQjxT20m6kLohbWRsGtbLa5W6-d7HhIr5FFFHOiL1GLe34qxooWOQxZxKuqJ_z_WVOtaDsCWOL2q6TcaXZ6Wf9UCzRBqJsD5sJds1OjACC9YKhr6QR4vVsUF2kpX0qPfh4REasj8_j7CR9xLz4v_oKqO8PzgT9_xuLMDiPxafa-MWh35ohJZ-7P0cwkCoetVxqwBVt06unxjrrV-QY8SOsq_AVi-J1hbqv3PK8XtW6TOwz6ghGYWg6Obs1-_pmpuc0gx_xWdKAApszLKrsSGLLIx_vovsfJ66VEana-q35x_dwaj4cN6X21w-ALznBRSD8Zg"
# TAL
    to = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjNpUVRWdE40TnBFLTlBSlRfNktMbmdQc2NYazFtM3ktLUNIUkR4dWdoM0kifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4tOXJuNXAiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjFiNTVkNzM4LWU2MjQtNDc5Zi1hNTVlLThiZTM2MWI4YzQzMiIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.nyc7Kr-jMdXQXR27Mbf44bOoYi5zVKJ0QqYO06jPj--_OUTEs388B3ylr3tXT79Mxc2P0uFR-_JoJ6fo6XMFKvSHbEkTtFpTfxUTfHSX5_GSGitp2u3SYpfEZ3Hva8Bk_VyD-Zg-c2-0381HbIHloPxh9J0nkjBIgG0rhgijOadDl2E9wWXqWn9ew4-SYaogmqyenweQesSf3iheyGtauP9lhxuJ_GR71IPZ96n27Jq1aiG0Ae-C9xp1Do9abNcNjGCZ2mduVqkSnKNBFRAKAJ-hHzyadqpz1tUoE-0NwwtqnxWF7DrQbFDpYIehY_ccHksqY3FwP1AnhiSGOLPaZQ"
#TAL
    ho = "127.0.0.1"
    ho = "192.168.50.184"
#GCP
#    ho = "35.189.92.255"

    #ho = "34.135.3.153"

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
    print ("create deployment")
    deploymentRes = client.ApplyDeployment(K8sGWRequest(fileName="yaml/hw.yaml", namespace="default", client_host=ho, client_port=po, client_token=to))
    print (deploymentRes)
    
    print ("create service ")
    serviceRes = client.ApplyService(K8sGWRequest(fileName="yaml/hello-world-service.yaml", namespace="default"))
    print (serviceRes)
    
    channel = grpc.insecure_channel("192.168.50.13:50051")
    client = K8sGWStub(channel)

    request = K8sGWRequest(
        user_id=1,  max_results=3
    )
    print (client.GetNSs(request))
    """
    #print (client.GetNSs(request))



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
