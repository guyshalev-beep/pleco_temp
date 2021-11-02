import os
import sys
import grpc
import subprocess
import yaml
from dataclasses import dataclass


@dataclass
class DataClassCluster:
    name: str = ""
    suffix: str = ""
    zone: str = ""
    region: str = ""
    externalIP: str = ""
    token: str = ""
    api_server: str = ""
    context: str = ""


class PlecoService(object):

    @staticmethod
    def create_follower(cluster_leader: DataClassCluster, cluster_follower: DataClassCluster, project_id, user_name):
        def printMsg(*msgs):
            os.system("echo ---------------------------------------------")
            for msg in msgs:
                os.system("echo ---- %s " % msg)
            os.system("echo ---------------------------------------------")

        printMsg('Start Leap Process')
        home_path = '/home/%s' % user_name[:user_name.find('@')]
        # Install Follower
        printMsg("Start To Spin Follower. [Leader Cluster is: %s , Follower: %s ]" % (
        cluster_leader.name, cluster_follower.name))
        os.system("terraform -chdir=../terraform/terraform_co_cluster/cluster_install init")
        os.system(
            "terraform -chdir=../terraform/terraform_co_cluster/cluster_install apply -var='suffix_name=%s' -var='zone=%s' -var='region=%s' -var='project_id=%s' -auto-approve" % (
            cluster_follower.suffix, cluster_follower.zone, cluster_follower.region, project_id))

        printMsg("Finished installing Follower: %s" % cluster_follower.name)

        # rolebindings:
        # printMsg("start to sleep")
        # os.system ("sleep 20s")
        os.system("gcloud container clusters get-credentials %s --zone %s --project %s" % (
        cluster_follower.name, cluster_follower.zone, project_id))
        cluster_follower.context = "gke_%s_%s_%s" % (project_id, cluster_follower.zone, cluster_follower.name)
        printMsg("Start To create clusterrolebindings for context: %s ]" % (cluster_follower.context))
        os.system(
            "kubectl --context %s create clusterrolebinding serviceaccounts-cluster-admin --clusterrole=cluster-admin --group=system:serviceaccounts" % (
                cluster_follower.context))
        os.system(
            "kubectl --context %s create clusterrolebinding user-admin-binding --clusterrole=cluster-admin --user=%s" % (
            cluster_follower.context, "$(gcloud config get-value account)"))

        # Add Firewall rule to Follower cluster
        printMsg("Add firewall rule on Follower: %s: ]" % (cluster_follower.name))
        os.system("terraform -chdir=../terraform/terraform_co_cluster/firewall_allow init")
        os.system(
            "terraform -chdir=../terraform/terraform_co_cluster/firewall_allow apply -var='suffix_name=%s' -var='zone=%s' -var='region=%s' -var='project_id=%s' -auto-approve" % (
            cluster_follower.suffix, cluster_follower.zone, cluster_follower.region, project_id))
        return [cluster_leader, cluster_follower]

    # install istio on follower
    @staticmethod
    def install_istio(cluster_leader: DataClassCluster, cluster_follower: DataClassCluster, project_id, user_name):
        def printMsg(*msgs):
            os.system("echo ---------------------------------------------")
            for msg in msgs:
                os.system("echo ---- %s " % msg)
            os.system("echo ---------------------------------------------")

        home_path = '/home/%s' % user_name[:user_name.find('@')]
        printMsg("start install pleco")
        os.system("export KUBECONFIG=${PWD}/istio-kubeconfig")
        s = "kubectl --context %s create clusterrolebinding user-admin-binding --clusterrole=cluster-admin --user=%s" % (
        cluster_follower.context, user_name)
        print(s)
        os.system(s)
        s = "kubectl --context %s create namespace istio-system" % cluster_follower.context
        os.system(s)
        # create the secret by using the appropriate certificate files
        s = "kubectl --context %s create secret generic cacerts -n istio-system --from-file=%s/istio-1.9.0/samples/certs/ca-cert.pem --from-file=%s/istio-1.9.0/samples/certs/ca-key.pem --from-file=%s/istio-1.9.0/samples/certs/root-cert.pem --from-file=%s/istio-1.9.0/samples/certs/cert-chain.pem;" % (
        cluster_follower.context, home_path, home_path, home_path, home_path)
        os.system(s)
        # Set Default Network
        s = "kubectl --context=%s label namespace istio-system topology.istio.io/network=network_%s" % (
        cluster_follower.context, cluster_follower.name)
        os.system(s)

        with open(r"istio_install.yaml") as file:
            doc = yaml.safe_load(file)
            doc['spec']['values']['global']['multiCluster']['clusterName'] = cluster_follower.name
            doc['spec']['values']['global']['network'] = "network_%s" % cluster_follower.name
            doc['spec']['components']['ingressGateways'][0]['label'][
                'topology.istio.io/network'] = "network_%s" % cluster_follower.name
            doc2 = [s for s in doc['spec']['components']['ingressGateways'][0]['k8s']['env'] if
                    s['name'] == "ISTIO_META_REQUESTED_NETWORK_VIEW"][0]
            doc2['value'] = "network_%s" % cluster_follower.name
            with open(r"istio_install_final.yaml", 'w') as file:
                result = yaml.dump(doc, file)
            os.system("istioctl install --context=%s -f istio_install_final.yaml -y" % cluster_follower.context)
            printMsg("Finished install Istion, sleep for 10s")
            os.system("sleep 10s")
        # Expose Services
        s = "kubectl --context=%s apply -n istio-system -f %s/istio-1.9.0/samples/multicluster/expose-services.yaml" % (
        cluster_follower.context, home_path)
        print(s)
        os.system(s)

    # Enable endpoint discovery on both clusters
    @staticmethod
    def enable_endpoint(cluster_leader: DataClassCluster, cluster_follower: DataClassCluster, project_id, user_name):
        s = "istioctl x create-remote-secret --context=%s --name=%s | kubectl apply -f - --context=%s" % (
        cluster_leader.context, cluster_leader.name, cluster_follower.context)
        print(s)
        os.system(s)
        s = "istioctl x create-remote-secret --context=%s --name=%s | kubectl apply -f - --context=%s" % (
        cluster_follower.context, cluster_follower.name, cluster_leader.context)
        print(s)
        os.system(s)

        # Install pleco on given cluster

    @staticmethod
    def install_pleco(cluster: DataClassCluster, project_id, user_name):
        def printMsg(*msgs):
            os.system("echo ---------------------------------------------")
            for msg in msgs:
                os.system("echo ---- %s " % msg)
            os.system("echo ---------------------------------------------")

        p = os.popen(
            "kubectl get nodes --context %s -o json | jq -r '.items[0]  | [.spec.nodeName,.metadata.name]' | grep gke | sed 's/\"//g'" % cluster.context)
        nodename = p.read()[2:-1]
        p = os.popen("kubectl --context %s get node %s -o jsonpath='{.status.addresses[?(@.type==\"%s\")].address}'" % (
        cluster.context, nodename, "InternalIP"))
        cluster.internalIP = p.read()
        command1 = "docker run -d -p %s:50051:50051 guypleco/gcp:latest" % cluster.internalIP
        os.system("gcloud beta compute ssh --zone \"%s\" \"%s\"  --project \"%s\" --command=\"%s\"" % (
        cluster.zone, nodename, project_id, command1))

        # printMsg("Leader Connections Params , API Server, Token", "internalIP=%s" % cluster_leader.internalIP, "ExternalIP=%s" % cluster_leader.externalIP, "API Server=%s" % cluster_leader.api_server, "TOKEN=%s" % cluster_leader.token)
        printMsg("Cluster Connections Params , Name=%s", "internalIP=%s" % cluster.name, cluster.internalIP,
                 "ExternalIP=%s" % cluster.externalIP, "API Server=%s" % cluster.api_server, "TOKEN=%s" % cluster.token)
