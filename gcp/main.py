import os
import sys
import time
import subprocess
from create_follower import PlecoService
from create_follower import DataClassCluster

param_leader_name = "pleco-326905-moon"
param_leader_zone = "europe-west2-b"
param_leader_region = "europe-west2"
param_leader_suffix = "-moon"
param_follower_name = "pleco-326905-moon-co"
param_follower_zone = "us-west2-b"
param_follower_region = "us-west2"
param_follower_suffix = "-moon-co"
param_plan_resource_file = "/home/pleco2309/pleco/plans/plan_sources.yaml"
param_plan_file = "/home/pleco2309/pleco/plans/plan_full.yaml"
param_istio_defaults = "/home/pleco2309/terraform/terraform_production/cluster1/istio-defaults.yaml"

number_of_leaps = sys.argv[1]
leap_period = sys.argv[2]  # in seconds
gcp_project_id = sys.argv[3]
user_name = sys.argv[4]
avoide_update_leader = sys.argv[5]  # if true, leader will not be installed (standalone for follower)
cross = sys.argv[6]  # if true, leader will be LEAP cluster and NOT the PRODUCTION cluster
avoid_delete_state = sys.argv[7]  # if true, Terraform state will not be deleted from follower scripts
avoide_delete_leader = sys.argv[
    8]  # if true, the leader cluster will remain - in case another leap is scheduled - it will definatly fail as the cluster is still there.
# python3 main.py 2 120 pleco-326905 pleco2309@shalev-family.com false false false false

print("Pleco Leap Trriger is set for %s leaps with period: %s" % (number_of_leaps, leap_period))
cluster_production = DataClassCluster(name=param_leader_name, zone=param_leader_zone, region=param_leader_region,
                                      suffix=param_leader_suffix)
cluster_leap = DataClassCluster(name=param_follower_name, zone=param_follower_zone, region=param_follower_region,
                                suffix=param_follower_suffix)
cluster_production.context = "gke_%s_%s_%s" % (gcp_project_id, cluster_production.zone, cluster_production.name)
cluster_leap.context = "gke_%s_%s_%s" % (gcp_project_id, cluster_leap.zone, cluster_leap.name)
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
    print("Pleco Leap number %d starts. Current time: %s %s" % (counter, local_time, time.tzname))
    print("***** leap from leader: \n********** %s \n***** to follower: \n********** %s" % (
    repr(cluster_leader), repr(cluster_follower)))
    #### clean all follower cluster terraform state
    if (avoid_delete_state != "true"):
        print("cleaning terraform state")
        os.system("find ../terraform/terraform_co_cluster -name \"*.tfstate*\" -type f -delete")
    #### create follower cluster

    result = PlecoService.create_follower(cluster_leader, cluster_follower, gcp_project_id, user_name)
    cluster_leader = result[0]
    cluster_follower = result[1]
    #### install istio on follower cluster
    result = PlecoService.install_istio(cluster_leader, cluster_follower, gcp_project_id, user_name)

    #### Enable endpoints on leader and follower clusters
    if (avoide_update_leader == "false"):
        result = PlecoService.enable_endpoint(cluster_leader, cluster_follower, gcp_project_id, user_name)

    #### install pleco on leader cluster
    if (avoide_update_leader == "false"):
        result = PlecoService.install_pleco(cluster_leader, gcp_project_id, user_name)
    #### install pleco on follower cluster
    result = PlecoService.install_pleco(cluster_follower, gcp_project_id, user_name)

    #### leap online-boutique app
    os.system("kubectl --context %s create namespace online-boutique" % cluster_follower.context)
    os.system("kubectl --context %s label namespace online-boutique istio-injection=enabled" % cluster_follower.context)
    os.system("kubectl apply -n online-boutique -f %s" % param_istio_defaults)
    os.system("python3 leap_online_boutique.py %s %s %s %s %s %s" % (
    cluster_leader.context, cluster_leader.suffix, cluster_follower.context, cluster_follower.suffix,
    param_plan_resource_file, param_plan_file))

    #### destroy leader cluster - TBD
    # os.system("echo Proceed? [y/n]: \n read -n 1 ans")
    if (avoide_delete_leader != "true"):
        os.system("gcloud container clusters delete %s -q --zone %s" % (cluster_leader.name, cluster_leader.zone))
        print("start delete firewall rule")
        os.system(
            "gcloud compute firewall-rules delete -q allow-all-%s-vpc%s" % (gcp_project_id, cluster_leader.suffix))
        print("start delete subnet")
        os.system("gcloud compute networks subnets delete -q %s-subnet%s --region %s" % (
        gcp_project_id, cluster_leader.suffix, cluster_leader.region))
        print("start delete vpc")
        os.system("gcloud compute networks delete %s-vpc%s -q" % (gcp_project_id, cluster_leader.suffix))

#### replace leader and follower
cluster_temp = cluster_leader
cluster_leader = cluster_follower
cluster_follower = cluster_temp
seconds_end = time.time()
local_time = time.ctime(seconds_end)
print("Pleco Leap number %d ends. Current time: %s %s, elapsed time: %d seconds." % (
counter, local_time, time.tzname, (seconds_end - seconds_start)))
print("-------------")
print("-------------")
print("-------------")
time.sleep(int(leap_period))
print("Pleco leap ended.")