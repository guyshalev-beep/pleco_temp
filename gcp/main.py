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

number_of_leaps = sys.argv[1]
leap_period = sys.argv[2]  # in seconds
gcp_project_id = sys.argv[3]
user_name = sys.argv[4]
cross = sys.argv[5]  # if true, leader will be LEAP cluster and NOT the PRODUCTION cluster
avoid_delete_state = sys.argv[6]  # if true, Terraform state will not be deleted from follower scripts
avoide_delete_leader = sys.argv[
    7]  # if true, the leader cluster will remain - in case another leap is scheduled - it will definatly fail as the cluster is still there.
# python3 main.py 1 0 pleco-326905 pleco2309@shalev-family.com true true true

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

    #### install pleco on follower cluster
    result = PlecoService.install_pleco(cluster_leader, cluster_follower, gcp_project_id, user_name)

    #### leap online-boutique app
    os.system("python3 leap_online_boutique.py %s %s %s %s %s" % (
    cluster_leader.context, cluster_leader.suffix, cluster_follower.context, cluster_follower.suffix,
    param_plan_resource_file, param_plan_file))

print("Pleco leap ended.")