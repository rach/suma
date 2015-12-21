

class ResourceWrapper(dict):
    def __init__(self, resource):
        self.resource = resource

    def unwrap(self):
        return self.resource
