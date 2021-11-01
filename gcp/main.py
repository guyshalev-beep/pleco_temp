import os
import sys
import time
import subprocess
from create_follower import PlecoService
from create_follower import DataClassCluster


number_of_leaps         = sys.argv[1]
leap_period             = sys.argv[2] # in seconds
gcp_project_id          = sys.argv[3]
user_name               = sys.argv[4]
cross                   = sys.argv[5] # if true, leader will be LEAP cluster and NOT the PRODUCTION cluster
avoid_delete_state      = sys.argv[6] # if true, Terraform state will not be deleted from follower scripts
avoide_delete_leader    = sys.argv[7] # if true, the leader cluster will remain - in case another leap is scheduled - it will definatly fail as the cluster is still there.
# python3 main.py 1 0 pleco-326905 pleco2309@shalev-family.com true true true

print ("Pleco Leap Trriger is set for %s leaps with period: %s"%(number_of_leaps,leap_period))
cluster_production  = DataClassCluster(name="pleco-326905-moon", zone="europe-west2-b", region="europe-west2", suffix="-moon")
cluster_leap        = DataClassCluster(name="pleco-326905-moon-co", zone="us-west2-b", region="us-west2", suffix = "-moon-co")
cluster_production.context = "gke_%s_%s_%s" %(gcp_project_id,cluster_production.zone,cluster_production.name)
cluster_leap.context = "gke_%s_%s_%s" %(gcp_project_id,cluster_leap.zone,cluster_leap.name)
# In the first time, leap from production (leader) to leap (follower)
cluster_leader = cluster_production
cluster_follower = cluster_leap
# Unless... cross is set to True
if (cross == "true"):
    cluster_leader = cluster_leap
    cluster_follower = cluster_production 

for counter in range(int(number_of_leaps)):
    seconds_start = time.time()	
    local_time = time.ctime(seconds_start)
    print ("Pleco Leap number %d starts. Current time: %s %s" %(counter,local_time, time.tzname))
    print ("***** leap from leader: \n********** %s \n***** to follower: \n********** %s" %(repr(cluster_leader),repr(cluster_follower)))
    #### clean all follower cluster terraform state
    if (avoid_delete_state != "true"):
        print("cleaning terraform state")
        os.system ("find ../terraform/terraform_co_cluster -name \"*.tfstate*\" -type f -delete")
    #### create follower cluster
    
    result  = PlecoService.create_follower(cluster_leader, cluster_follower, gcp_project_id, user_name)
    cluster_leader = result[0]
    cluster_follower = result[1]
    #### install istio on follower cluster
    result = PlecoService.install_istio(cluster_leader, cluster_follower, gcp_project_id, user_name)
    
    #### install pleco on follower cluster
    result = PlecoService.install_pleco(cluster_leader, cluster_follower, gcp_project_id, user_name)
    
    #### leap online-boutique app
    
    """
    #### leap online-boutique app
    print ("Pleco Leap number %d starts. Current time: %s %s" %(counter,local_time, time.tzname))
    print ("***** leap from leader: \n********** %s \n***** to follower: \n********** %s" %(repr(cluster_leader),repr(cluster_follower)))
    os.system("python3 leap_online_boutique.py %s %s %s %s %s %s %s %s %s %s %s"%(
        cluster_leader.name, cluster_leader.zone, cluster_leader.externalIP, cluster_leader.token,cluster_leader.api_server,
        cluster_follower.name, cluster_follower.zone, cluster_follower.externalIP, cluster_follower.token,cluster_follower.api_server,
        gcp_project_id))
    
    #### set load balancer to follower - TBD
    # update the LB to Co Cluster
    p = os.popen("kubectl --context %s get -n istio-system service istio-ingressgateway -o json | jq -r '.status.loadBalancer.ingress[0].ip'" %cluster_follower.context)
    endpoint_ip=p.read()
    print("Setting load balancer to follower endpoint: %s" %endpoint_ip)
    #os.system("echo Proceed? [y/n]: \n read -n 1 ans")
    endpoind_group_name_follower = "plecoendpointgroup%s"%cluster_follower.suffix
    endpoind_group_name_leader = "plecoendpointgroup%s"%cluster_leader.suffix
    endpoint_backend = "plecobeservice"
    # Create a new endpoint group for the new cluster
    os.system("gcloud compute network-endpoint-groups delete -q %s --global" % endpoind_group_name_follower)
    os.system("gcloud compute network-endpoint-groups create %s --global --network-endpoint-type=\"internet-ip-port\" --default-port=80" % endpoind_group_name_follower)
    # Set up the IP of the new Cluster in the newly created endpoint group
    os.system("gcloud compute network-endpoint-groups update %s --global --add-endpoint=ip=%s,port=80" % (endpoind_group_name_follower, endpoint_ip))
    # Remove the old endpoint group of the old cluster from the backend service that is connected to the LB
    # This will create a downtime and NEED TO BE FIXED
    os.system("gcloud compute backend-services remove-backend %s --network-endpoint-group=%s --global-network-endpoint-group --global" % (endpoint_backend,endpoind_group_name_leader))
    # Add the newly created endpoint group of the new cluster to (allready exists) endpoint Backend   
    os.system("gcloud compute backend-services add-backend %s --network-endpoint-group=%s --global-network-endpoint-group --global" % (endpoint_backend,endpoind_group_name_follower))
    # clean the old endpoint group
    os.system("gcloud compute network-endpoint-groups delete -q %s --global" % endpoind_group_name_leader)
    #### destroy leader cluster 
    #os.system("echo Proceed? [y/n]: \n read -n 1 ans")
    if (avoide_delete_leader != "true"):
        os.system("gcloud container clusters delete %s -q --zone %s"%(cluster_leader.name,cluster_leader.zone))
        print("start delete firewall rule")
        os.system("gcloud compute firewall-rules delete -q allow-all-%s-vpc%s"%(gcp_project_id,cluster_leader.suffix))
        print("start delete subnet")
        os.system("gcloud compute networks subnets delete -q %s-subnet%s --region %s"%(gcp_project_id,cluster_leader.suffix,cluster_leader.region))
        print("start delete vpc")
        os.system("gcloud compute networks delete %s-vpc%s -q"%(gcp_project_id,cluster_leader.suffix))
    #### replace leader and follower
    cluster_temp = cluster_leader
    cluster_leader = cluster_follower
    cluster_follower = cluster_temp
    seconds_end = time.time()
    local_time = time.ctime(seconds_end)
    print ("Pleco Leap number %d ends. Current time: %s %s, elapsed time: %d seconds." %(counter,local_time, time.tzname, (seconds_end-seconds_start)))       
    print("-------------")
    print("-------------")
    print("-------------")
    time.sleep (int(leap_period) )
    """
print ("Pleco leap ended.")