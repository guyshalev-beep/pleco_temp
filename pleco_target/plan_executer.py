import yaml
import os
import sys
from loader import Loader
from deploment_handler import DeploymentHandler
from service_handler import ServiceHandler
from redis_handler import RedisHandler
from loadbalancer_handler import LoadBalancerHandler
from filesystem_repository_handler import FilesystemRepositoryHandler


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.




# python3 plan_executer.py /home/pleco2110/pleco/plans/plan_a.yaml
class PlanExecuter(object):
    plan_file = ""
    def __init__(self, plan_file):
        self.plan_file = plan_file
        print("Started Plan Executer with plan:%s" % plan_file)
        pass

    if __name__ == '__main__':
        if (len(sys.argv) > 1):
            plan_file = sys.argv[1]
        if (plan_file == ""):
            plan_file = './pleco_target/plans/plan_a.yaml'

        pass

    def execute(self):
        with open(r"%s"%self.plan_file) as file:
            documents = yaml.load(file, Loader)
            handlers_doc = documents.get('handlers')
            sources_doc = documents.get('sources')
            plan = documents.get('plan')

            for plan_step_doc in plan:
                handler = plan_step_doc['handler']
                method = plan_step_doc['method']
                print ("Start processing: %s" %(plan_step_doc['resource']['name']))
                print ("  - Type: %s" % (plan_step_doc['resource']['type']))
                print("  - Method: %s" % (method))
                # Repository Handler
                repository_handler = self.get_repository_handler(plan_step_doc, method)
                # select the specific resource handler doc which its TYPE equals the plan step's RESOURCE.HANDLER
                if plan_step_doc['resource']['handler'] != None:
                    repository_handler_doc = [s for s in handlers_doc if s['type'] == plan_step_doc['resource']['handler']][0]
                    body = repository_handler.handle(repository_handler_doc, plan_step_doc);
                    plan_step_doc['resource']['body'] = body

                # Handler
                handler_object = DeploymentHandler()  # default
                if handler == "DeploymentHandler":
                    handler_object = DeploymentHandler()
                if handler == "ServiceHandler":
                    handler_object = ServiceHandler()
                if handler == "RedisHandler":
                    handler_object = RedisHandler()
                if handler == "GCPLoadBalancerHandler":
                    handler_object = LoadBalancerHandler()
                handler_object.handle(sources_doc, plan_step_doc)

    def get_repository_handler(self, plan_step_doc, method):
        repository_handler_name = plan_step_doc['resource']['handler']
        if repository_handler_name == 'FilesystemRepositoryHandler':
            return FilesystemRepositoryHandler(method)
        elif repository_handler_name == 'VaultRepositoryHandler':
            pass
        pass
