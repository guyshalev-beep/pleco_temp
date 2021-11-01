from os import path
import sys
import yaml

class FilesystemRepositoryHandler(object):
    def __init__(self, method):
        #print("start FilesystemRepositoryHandler.")
        pass

    def handle(self, handler_doc, step_doc):
        #print ("start file handling")
#        print(handler_doc)
#        print(step_doc)
        try:
            fileName = step_doc['resource']['path']
            directoryName = handler_doc['directory']
            resource_path = directoryName + fileName
            print("opening resource file:%s"%resource_path)
            with open(path.join(path.dirname(__file__), resource_path)) as f:
                dep = yaml.safe_load(f)
            return dep
        except:
            e = sys.exc_info()
            print(e)
            return ""
