import time
import os
import sys
import grpc
sys.path.append("./pleco_target")
from pleco_target_pb2 import K8sGWRequest
from pleco_target_pb2_grpc import K8sGWStub

def createService(*resource_names, client, api_server, token):
    for resource_name in resource_names:
        print("start deploy service %s" % resource_name)
        service_res = client.ApplyService(
            K8sGWRequest(fileName="yaml/services/%s-svc.yaml" % resource_name, namespace="online-boutique",
                         client_host=api_server,
                         client_port=port,
                         client_token=token))
        print(service_res)


def createResource(*resource_names, client, api_server, token):
    for resource_name in resource_names:
        print("start deploy %s" % resource_name)
        deployment_res = client.ApplyDeployment(
            K8sGWRequest(fileName="yaml/deployments/%s-deployment.yaml" % resource_name, namespace="online-boutique",
                         client_host=api_server, client_port=port,
                         client_token=token))
        print(deployment_res)
        os.system("kubectl -n online-boutique wait --for=condition=available deployment %s --timeout=5m" %(resource_name))
        service_res = client.ApplyService(
            K8sGWRequest(fileName="yaml/services/%s-svc.yaml" % resource_name, namespace="online-boutique",
                         client_host=api_server,
                         client_port=port,
                         client_token=token))
        print(service_res)

def deleteResource(*resource_names, client, api_server, token):
    for resource_name in resource_names:
        print("start delete %s" % resource_name)
        deploymentRes = client.DeleteDeployment(
            K8sGWRequest(resourceName=resource_name, namespace="online-boutique", client_host=api_server,
                         client_port=port,
                         client_token=token))
        print(deploymentRes)
  #      serviceRes = client.DeleteService(
  #          K8sGWRequest(resourceName=resource_name, namespace="online-boutique", client_host=api_server,
  #                       client_port=po,
  #                       client_token=token))
  #      print(serviceRes)

def leapResource(*resource_names, client_leader, client_follower, api_server_leader, api_server_follower,
                 token_leader, token_follower):
    for resource_name in resource_names:
        print("apply %s on follower." % resource_name)
        createResource(resource_name, client=client_follower, api_server=api_server_follower,
                       token=token_follower)
        #time.sleep(10)
        
        print("remove %s from leader." % resource_name)
        deleteResource(resource_name, client=client_leader, api_server=api_server_leader, token=token_leader)

def leapRedis(client_leader, client_follower, api_server_leader, api_server_follower,
                 token_leader, token_follower, cluster_name_leader, cluster_name_follower, zone_leader, zone_follower, project_id):
    print("Create redis_cart on follower")
    createResource("redis-cart", client=client_follower, api_server=api_server_follower,
                       token=token_follower)
    print("Start sync_redis")
    os.system("python3 sync_redis.py %s %s %s %s %s online-boutique" %(cluster_name_leader, zone_leader, cluster_name_follower, zone_follower, project_id))
    print("Create cartservice on follower")
    createResource("cartservice", client=client_follower, api_server=api_server_follower,
                       token=token_follower) 
    deleteResource("redis-cart", client=client_leader, api_server=api_server_leader, token=token_leader)
    os.system("python3 remove_old_redis.py %s %s %s %s %s online-boutique" %(cluster_name_leader,zone_leader, cluster_name_follower, zone_follower, project_id))
    deleteResource("cartservice", client=client_leader, api_server=api_server_leader, token=token_leader)

if __name__ == '__main__':
    
    cluster_name_leader     = sys.argv[1]
    zone_leader             = sys.argv[2]
    external_ip_leader      = sys.argv[3]
    token_leader            = sys.argv[4]
    api_server_leader       = sys.argv[5]
    cluster_name_follower   = sys.argv[6]
    zone_follower           = sys.argv[7]    
    external_ip_follower    = sys.argv[8]
    token_follower          = sys.argv[9]
    api_server_follower     = sys.argv[10]
    gcp_project_id          = sys.argv[11]
    client_leader           = K8sGWStub(grpc.insecure_channel("%s:50051"%external_ip_leader))
    client_follower         = K8sGWStub(grpc.insecure_channel("%s:50051"%external_ip_follower))
    port                    = "443"

    print("Test Connection to Leader")
    ret = client_leader.TestConnection(K8sGWRequest())
    print(ret)

    print("Test Connection to Follower")
    ret = client_follower.TestConnection(K8sGWRequest())
    print(ret)
    
    print("Create namespace online-boutique on Follower")
    context_follower = "gke_%s_%s_%s" %(gcp_project_id,zone_follower,cluster_name_follower)
    os.system("kubectl --context %s create namespace online-boutique" %context_follower)
    os.system("kubectl --context %s label namespace online-boutique istio-injection=enabled" %context_follower)
    os.system("kubectl --context %s -n online-boutique apply -f ./../terraform/resources/istio-defaults_online-boutique.yaml" %context_follower)

    # Leap some services
    leapResource("adservice", "checkoutservice", "currencyservice", "emailservice", "paymentservice", "shippingservice",
                 client_leader=client_leader, client_follower=client_follower,
                 api_server_leader=api_server_leader, api_server_follower=api_server_follower,
                 token_leader=token_leader, token_follower=token_follower)
   
    # leap Redis  
    leapRedis(client_leader=client_leader, client_follower=client_follower,
                 api_server_leader=api_server_leader, api_server_follower=api_server_follower,
                 token_leader=token_leader, token_follower=token_follower,
                 cluster_name_leader=cluster_name_leader, cluster_name_follower=cluster_name_follower, zone_leader=zone_leader, zone_follower=zone_follower,
                 project_id=gcp_project_id)

    # leap rest
    leapResource("productcatalogservice", "recommendationservice","frontend",
                 client_leader=client_leader, client_follower=client_follower,
                 api_server_leader=api_server_leader, api_server_follower=api_server_follower,
                 token_leader=token_leader, token_follower=token_follower)