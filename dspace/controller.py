import os
from typing import Dict

from dspace.client import DockerClient
from dspace.config import ConfigStore
from dspace.flavours import Flavour, flavour_map


class DSpaceController:
    """
    Controller for dataspaces; allows users to issue commands through the CLI or other
    frontend.

    """

    _container_name_prefix: str = "dspace_"

    _db_flavours: Dict[str, Flavour] = flavour_map

    def __init__(self) -> None:
        self.docker_client = DockerClient()

    def get_space_flavour(self, space_name):
        container_name = f"{self._container_name_prefix}{space_name}"
        container = self.docker_client.get_container(container_name)
        assert container, f"There was no container with the name {container_name}"

        image_name = container.attrs["Config"]["Image"]
        flavour_filtered = [
            flavour
            for flavour in self._db_flavours.values()
            if flavour.container_image == image_name
        ]

        assert (
            flavour_filtered
        ), f"There is no space flavour matching the image {image_name}"

        return flavour_filtered[0]

    def setup(self):
        self.docker_client.ensure_network_exists()
        ConfigStore.setup()

    def load_config(self):
        """
        Load the file-based DSpace configuration
        """
        self._config = ConfigStore.get_or_create()

    def create(
        self, space_name: str, expose_port: int, flavour: str, initial_database: str
    ):
        assert (
            flavour in self._db_flavours
        ), f"That database flavour was not supported. Accepted flavours: {self._db_flavours.keys()}"

        self.load_config()

        flavour = self._db_flavours[flavour]

        container_name = f"{self._container_name_prefix}{space_name}"

        volume_directory = os.path.join(self._config._config_folder, 'volumes', space_name)
        if not os.path.exists(volume_directory):
            os.makedirs(volume_directory, exist_ok=True)

        self.docker_client.create_container(
            name=container_name,
            expose_port=expose_port,
            flavour=flavour,
            database=initial_database,
            user=self._config.default_user,
            password=self._config.default_password,
            volume_directory=volume_directory
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

    def spawn_shell(self, space_name: str):
        cmd = f"docker exec -it {self._container_name_prefix}{space_name} /bin/bash"
        os.system(cmd)

    def dba(self, space_name: str):
        flavour = self.get_space_flavour(space_name)
        cmd = (
            f"docker exec -it {self._container_name_prefix}{space_name} "
            f"/bin/bash -c {flavour.repl_command}"
        )

        os.system(cmd)
