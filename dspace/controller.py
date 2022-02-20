from typing import Dict

from dspace.client import DockerClient
from dspace.config import ConfigStore
from dspace.flavours import flavour_map, Flavour


class DSpaceController:
    """
    Controller for dataspaces; allows users to issue commands through the CLI or other
    frontend.

    """

    _container_name_prefix: str = "dspace_"

    _db_flavours: Dict[str, Flavour] = flavour_map

    def __init__(self) -> None:
        self.docker_client = DockerClient()

    def setup(self):
        self.docker_client.ensure_network_exists()
        ConfigStore.setup()

    def load_config(self):
        """
        Load the file-based DSpace configuration
        """

        self._config = ConfigStore.get_or_create()

    def create(self, space_name: str, expose_port: int, flavour: str, initial_database: str):
        assert (
            flavour in self._db_flavours
        ), f"That database flavour was not supported. Accepted flavours: {self._db_flavours.keys()}"

        self.load_config()

        flavour = self._db_flavours[flavour]

        container_name = f"{self._container_name_prefix}{space_name}"

        self.docker_client.create_container(
            name=container_name,
            expose_port=expose_port,
            flavour=flavour,
            database=initial_database,
            user=self._config.default_user,
            password=self._config.default_password,
        )

    def kill(self, space_name: str):
        container_name = f"{self._container_name_prefix}{space_name}"

        self.docker_client.kill_container(container_name)

    def pause(self, space_name: str):
        container_name = f"{self._container_name_prefix}{space_name}"

        self.docker_client.pause_container(name=container_name)

    def resume(self, space_name: str):
        container_name = f"{self._container_name_prefix}{space_name}"
        self.docker_client.resume_container(name=container_name)

    def list_dataspaces(self, active_only: bool = False):
        return self.docker_client.list_containers(active_only)

    def killall(self):
        self.docker_client.killall()
