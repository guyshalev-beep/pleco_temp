import yaml
import os
import sys


def generate_sources_file(cluster_leader_context, cluster_leader_suffix, cluster_follower_context,
                          cluster_follower_suffix, plan_file):
    # Extract detailes on Clusters
    #       cluster_leader_context = "gke_%s_%s_%s" % (project_id, cluster_leader.zone, cluster_leader.name)
    p = os.popen(
        "kubectl get nodes --context %s -o json | jq -r '.items[0]  | [.spec.nodeName,.metadata.name]' | grep gke | sed 's/\"//g'" % cluster_leader_context)
    nodename_leader = p.read()[2:-1]
    p = os.popen("kubectl --context %s get node %s -o jsonpath='{.status.addresses[?(@.type==\"%s\")].address}'" % (
        cluster_leader_context, nodename_leader, "InternalIP"))
    cluster_leader_internalIP = p.read()
    p = os.popen("kubectl --context %s get node %s -o jsonpath='{.status.addresses[?(@.type==\"%s\")].address}'" % (
        cluster_leader_context, nodename_leader, "ExternalIP"))
    cluster_leader_externalIP = p.read()
    print("Leader Node details: ", cluster_leader_context, nodename_leader, cluster_leader_internalIP,
          cluster_leader_externalIP)

    p = os.popen(
        "kubectl config view -o jsonpath='{.clusters[?(@.name==\"%s\")].cluster.server}'" % (cluster_leader_context))
    cluster_leader_api_server = p.read()[8:]  # remove https://
    print("Leader Cluster API Server:", cluster_leader_api_server)
    p = os.popen(
        "kubectl --context %s get secrets -o jsonpath=\"{.items[?(@.metadata.annotations['kubernetes\.io/service-account\.name']=='default')].data.token}\"|base64 --decode" % (
            cluster_leader_context))
    cluster_leader_token = p.read()
    print("Leader Cluster TOKEN:", cluster_leader_token)

    #        cluster_follower_context = "gke_%s_%s_%s" % (project_id, cluster_follower.zone, cluster_follower.name)
    p = os.popen(
        "kubectl get nodes --context %s -o json | jq -r '.items[0]  | [.spec.nodeName,.metadata.name]' | grep gke | sed 's/\"//g'" % cluster_follower_context)
    nodename_follower = p.read()[2:-1]
    p = os.popen("kubectl --context %s get node %s -o jsonpath='{.status.addresses[?(@.type==\"%s\")].address}'" % (
        cluster_follower_context, nodename_follower, "InternalIP"))
    cluster_follower_internalIP = p.read()
    p = os.popen("kubectl --context %s get node %s -o jsonpath='{.status.addresses[?(@.type==\"%s\")].address}'" % (
        cluster_follower_context, nodename_follower, "ExternalIP"))
    cluster_follower_externalIP = p.read()
    print("Follower Node details:", cluster_follower_context, nodename_follower, cluster_follower_internalIP,
          cluster_follower_externalIP)
    p = os.popen(
        "kubectl config view -o jsonpath='{.clusters[?(@.name==\"%s\")].cluster.server}'" % (cluster_follower_context))
    cluster_follower_api_server = p.read()[8:]  # remove https://
    print("Follower Cluster API Server:", cluster_follower_api_server)
    p = os.popen(
        "kubectl --context %s get secrets -o jsonpath=\"{.items[?(@.metadata.annotations['kubernetes\.io/service-account\.name']=='default')].data.token}\"|base64 --decode" % (
            cluster_follower_context))
    cluster_follower_token = p.read()
    print("Follower Cluster TOKEN:", cluster_follower_token)

    dict_file = [{'name': 'leader_source', 'id': 'leader_source_id', 'suffix': cluster_leader_suffix,
                  'externalIP': cluster_leader_externalIP,
                  'token': cluster_leader_token, 'api_server': cluster_leader_api_server, 'port': '443',
                  'context': cluster_leader_context},
                 {'name': 'follower_source', 'id': 'follower_source_id', 'suffix': cluster_follower_suffix,
                  'externalIP': cluster_follower_externalIP,
                  'token': cluster_follower_token, 'api_server': cluster_follower_api_server, 'port': '443',
                  'context': cluster_follower_context}
                 ]

    with open(r"%s" % plan_file, 'w') as file:
        documents = yaml.dump(dict_file, file)
    print("dump")


# python3 plan_generator.py gke_pleco-326905_europe-west2-b_pleco-326905-moon -moon gke_pleco-326905_us-west2-b_pleco-326905-moon-co -moon-co /home/pleco2309/pleco/plans/plan_sources.yaml

class PlanGenerator(object):
    cluster_leader_context = sys.argv[1]
    cluster_leader_suffix = sys.argv[2]
    cluster_follower_context = sys.argv[3]
    cluster_follower_suffix = sys.argv[4]
    plan_file = sys.argv[5]

    def __init__(self, cluster_leader_context,cluster_leader_suffix, cluster_follower_context, cluster_follower_suffix,plan_file):
        # print("start FilesystemRepositoryHandler.")
        self.cluster_leader_context = cluster_leader_context
        self.cluster_leader_suffix = cluster_leader_suffix
        self.cluster_follower_context = cluster_follower_context
        self.cluster_follower_suffix =  cluster_follower_suffix
        self.plan_file = plan_file
        pass

    if __name__ == '__main__':
        generate_sources_file(cluster_leader_context, cluster_leader_suffix, cluster_follower_context,
                              cluster_follower_suffix, plan_file)

    def generate(self):
        generate_sources_file(self.cluster_leader_context, self.cluster_leader_suffix, self.cluster_follower_context,
                              self.cluster_follower_suffix, self.plan_file)