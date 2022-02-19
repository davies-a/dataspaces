from dspace.config import ConfigStore
from dspace.client import DockerClient


class DSpaceController:
    """
    Controller for dataspaces; allows users to issue commands through the CLI or other
    frontend.

    """

    _container_name_prefix: str = "dspace_"

    _db_flavours = {"postgres": "postgres:14"}

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

    def create(self, space_name, expose_port, flavour, initial_database):
        assert (
            flavour in self._db_flavours
        ), f"That database flavour was not supported. Accepted flavours: {self._db_flavours.keys()}"

        self.load_config()

        db_image = self._db_flavours[flavour]

        container_name = f"{self._container_name_prefix}{space_name}"

        self.docker_client.create_container(
            name=container_name,
            expose_port=expose_port,
            container_image=db_image,
            initial_database=initial_database,
            initial_user=self._config.default_user,
            initial_password=self._config.default_password,
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

    def list_dataspaces(self, active_only):
        return self.docker_client.list_containers(active_only)

    def killall(self):
        self.docker_client.killall()
