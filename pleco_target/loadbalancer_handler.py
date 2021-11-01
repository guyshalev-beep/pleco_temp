import os
import grpc
import sys

sys.path.append("./pleco_target")
from pleco_target_pb2 import K8sGWRequest
from pleco_target_pb2_grpc import K8sGWStub


def handle_leap(sources_doc, step_doc):
    leader_source = [s for s in sources_doc if s['name'] == "leader_source"][0]
    follower_source = [s for s in sources_doc if s['name'] == "follower_source"][0]

    #### set load balancer to follower - TBD
    # Retrieve the IP from the target service in the leader cluster
    to_ns = step_doc['resource']['target_service']['namespace']
    to_service = step_doc['resource']['target_service']['service_name']
    exac_str = "kubectl --context %s get -n %s service %s -o json | jq -r '.status.loadBalancer.ingress[0].ip'" % (follower_source['context'],to_ns, to_service)
    print(exac_str)
    p = os.popen(exac_str)
    to_endpoint_ip = p.read()
    print("Setting load balancer to follower endpoint: %s" % to_endpoint_ip)
    endpoind_group_name_follower = "%s%s" % (step_doc['resource']['endpoint_group_name'], follower_source['suffix'])
    endpoind_group_name_leader = "%s%s" % (step_doc['resource']['endpoint_group_name'], leader_source['suffix'])
    backend_service = step_doc['resource']['backend_service']
    target_port = step_doc['resource']['target_port']
    print("endpoind_group_name_leader=%s"%endpoind_group_name_leader)
    print("endpoind_group_name_follower=%s" % endpoind_group_name_follower)
    print("backend_service=%s" % backend_service)
    print("target_port=%s" % target_port)
    # Create a new endpoint group for the new cluster
    os.system("gcloud compute network-endpoint-groups delete -q %s --global" % endpoind_group_name_follower)
    os.system(
        "gcloud compute network-endpoint-groups create %s --global --network-endpoint-type=\"internet-ip-port\" --default-port=%s" % (endpoind_group_name_follower, target_port))
    # Set up the IP of the new Cluster in the newly created endpoint group
    os.system("gcloud compute network-endpoint-groups update %s --global --add-endpoint=ip=%s,port=%s" %(endpoind_group_name_follower, to_endpoint_ip,target_port))
    # Remove the old endpoint group of the old cluster from the backend service that is connected to the LB
    # This will create a downtime and NEED TO BE FIXED
    os.system(
        "gcloud compute backend-services remove-backend %s --network-endpoint-group=%s --global-network-endpoint-group --global" %(
        backend_service, endpoind_group_name_leader))
    # Add the newly created endpoint group of the new cluster to (allready exists) endpoint Backend
    os.system(
        "gcloud compute backend-services add-backend %s --network-endpoint-group=%s --global-network-endpoint-group --global" %(
        backend_service, endpoind_group_name_follower))
    # clean the old endpoint group
    os.system("gcloud compute network-endpoint-groups delete -q %s --global" % endpoind_group_name_leader)


class LoadBalancerHandler(object):


    def handle(self, sources_doc, step_doc):
        method = step_doc['method']
        print("start LoadBalancerHandler handling with method=%s" % method)
        if method == 'leap':
            return handle_leap(sources_doc, step_doc)
  #      if method == 'standalone':
 #           return handle_standalone(sources_doc, step_doc)
        return None