import time
import os
import sys
import grpc

sys.path.append("./pleco/pleco_target/")
from plan_generator import PlanGenerator
from plan_executer import PlanExecuter

# python3 leap_online_boutique.py gke_pleco-326905_europe-west2-b_pleco-326905-moon -moon gke_pleco-326905_us-west2-b_pleco-326905-moon-co -moon-co /home/pleco2309/pleco/plans/plan_sources.yaml /home/pleco2309/pleco/plans/plan_a.yaml

if __name__ == '__main__':
    cluster_context_leader = sys.argv[1]
    cluster_suffix_leader = sys.argv[2]
    cluster_context_follower = sys.argv[3]
    cluster_suffix_follower = sys.argv[4]
    plan_sources_file = sys.argv[5]
    plan_file = sys.argv[6]

    print("Start to leap online-boutique")
    # Generate Plan's sources (leader and follower)

    pg = PlanGenerator(cluster_context_leader, cluster_suffix_leader, cluster_context_follower, cluster_suffix_follower,
                       plan_sources_file)
    pg.generate()
    pe = PlanExecuter(plan_file)
    pe.execute()
