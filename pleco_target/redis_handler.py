import os
import grpc
import sys

sys.path.append("./pleco_target")
from pleco_target_pb2 import K8sGWRequest
from pleco_target_pb2_grpc import K8sGWStub


def handle_leap_to_new_cluster(sources_doc, step_doc):
    #leader_source = sources_doc['name' == 'leader_source']
    leader_source = [s for s in sources_doc if s['name'] == "leader_source"][0]
    #follower_source = sources_doc['name' == 'follower_source']
    follower_source = [s for s in sources_doc if s['name'] == "follower_source"][0]
    yaml = step_doc['resource']['body']
    leader_client = K8sGWStub(grpc.insecure_channel("%s:50051" % leader_source['externalIP']))
    follower_client = K8sGWStub(grpc.insecure_channel("%s:50051" % follower_source['externalIP']))
    ns = step_doc['resource']['namespace']
    resource_name = step_doc['resource']['name']
    print("start REDIS handle_leap_to_new_cluster for:%s from leader:%s to follower:%s" % (resource_name,leader_source['externalIP'], follower_source['externalIP']))
    # Create on follower
    deployment_res = follower_client.ApplyDeployment(
        K8sGWRequest(body=str(yaml), namespace=ns, client_host=follower_source['api_server'], client_port=str(follower_source['port']),
                     client_token=follower_source['token']))
    print(deployment_res)
    os.system("kubectl --context %s -n %s wait --for=condition=available deployment %s --timeout=1m" % (follower_source['context'],ns, resource_name))

    p = os.popen("kubectl --context %s -n %s get pods -o custom-columns=PodName:.metadata.name | grep redis" % (follower_source['context'],ns))
    redis_pod = p.read()[:-1]

    print("REDIS ready with POD = %s" % redis_pod)
    exac_str = "kubectl --context %s -n %s exec -it %s -- redis-cli replicaof redis-cart 6379" % (follower_source['context'],ns, redis_pod)
    print(exac_str)
    os.system(exac_str)
    print ("Synced Redis. go to sleep.")
    os.system("sleep 10s")
    exac_str = "kubectl --context %s -n %s exec -it %s -- redis-cli REPLICAOF NO ONE" % (follower_source['context'],ns, redis_pod)
    print(exac_str)
    os.system(exac_str)
    print("Stopped ReplicaOf Redis.")
    # Delete from Leader
    deploymentRes = leader_client.DeleteDeployment(
        K8sGWRequest(resourceName=resource_name, namespace=ns, client_host=leader_source['api_server'],
                     client_port=str(leader_source['port']),
                     client_token=leader_source['token']))
    print(deploymentRes)
# Standalone for redis does not involve any sync. It looks like Standalone Deployment.
def handle_standalone(sources_doc, step_doc):
    # deploy to follower source
    source = [s for s in sources_doc if s['name'] == "follower_source"][0]
    yaml = step_doc['resource']['body']
    follower_client = K8sGWStub(grpc.insecure_channel("%s:50051" % source['externalIP']))
    ns = step_doc['resource']['namespace']
    resource_name = step_doc['resource']['name']
    print("start REDIS handle_standalone for:%s to follower:%s" % (resource_name,source['externalIP']))
    # Create on follower
    deployment_res = follower_client.ApplyDeployment(
        K8sGWRequest(body=str(yaml), namespace=ns,
                     client_host=source['api_server'], client_port=str(source['port']),
                     client_token=source['token']))
    print(deployment_res)
    os.system("kubectl -n %s wait --for=condition=available deployment %s --timeout=1m" % (ns, resource_name))

class RedisHandler(object):
    def __init__(self):
        print("start RedisHandler")
        pass

    def handle(self, sources_doc, step_doc):
        method = step_doc['method']
        print("start REDIS handling with method=%s" % method)
        if method == 'leap_to_new_cluster':
            return handle_leap_to_new_cluster(sources_doc, step_doc)
        if method == 'standalone':
            return handle_standalone(sources_doc, step_doc)
        return None