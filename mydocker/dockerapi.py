import docker
from docker.types import ServiceMode

class DockerAPIWrapper(object):
  def __init__(self, client = None):
    self.client = client or docker.from_env()

    def _get_service(self, service_name):
      services = self.client.services.list(filters=dict(name=service_name))
      return services[0]

    def getReplicaCount(self, service_name):
      service = self._get_service(service_name)
      return service.attrs['Spec']['Mode']['Replicated']['Replicas']

    def scaleService(self, service_name, replica_count):
      service = self._get_service(service_name)
      service.update(mode=ServiceMode("replicated", replicas=replica_count))
