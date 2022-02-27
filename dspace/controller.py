import os
import subprocess
from typing import Dict, Optional
import shutil

from dspace.client import DockerClient
from dspace.config import ConfigStore
from dspace.flavours import Flavour, flavour_map
from dspace.snapshots import SnapshotController


class DSpaceController:
    """
    Controller for dataspaces; allows users to issue commands through the CLI or other
    frontend.

    """

    _container_name_prefix: str = "dspace_"
    _config: ConfigStore

    _db_flavours: Dict[str, Flavour] = flavour_map
    docker_client = DockerClient()

    _snapshot_controller: SnapshotController

    def __init__(self):
        self._config = ConfigStore.get_or_create()
        self._snapshot_controller = SnapshotController(self._config)

    @classmethod
    def setup(cls):
        cls.docker_client.ensure_network_exists()
        ConfigStore.setup()

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

    def get_volume_directory_for_space(self, space_name: str) -> str:
        volume_directory = os.path.join(
            self._config._config_folder, "volumes", space_name
        )
        if not os.path.exists(volume_directory):
            os.makedirs(volume_directory, exist_ok=True)

        return volume_directory

    def get_snapshot_directory(self, snapshot_name: Optional[str] = None) -> str:
        return self._snapshot_controller.get_snapshot_directory(snapshot_name)

    def create(
        self, space_name: str, expose_port: int, flavour: str, initial_database: str
    ):
        assert (
            flavour in self._db_flavours
        ), f"That database flavour was not supported. Accepted flavours: {self._db_flavours.keys()}"

        flavour = self._db_flavours[flavour]

        container_name = f"{self._container_name_prefix}{space_name}"

        volume_directory = self.get_volume_directory_for_space(space_name=space_name)

        self.docker_client.create_container(
            name=container_name,
            expose_port=expose_port,
            flavour=flavour,
            database=initial_database,
            user=self._config.default_user,
            password=self._config.default_password,
            volume_directory=volume_directory,
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

    def make_snapshot(self, snapshot_name, space_name, update: Optional[bool] = False):
        volume_directory = self.get_volume_directory_for_space(space_name=space_name)
        snapshot_directory = self.get_snapshot_directory(snapshot_name=snapshot_name)
        existed = self._snapshot_controller.get_snapshot(snapshot_name) is not None

        if existed and update is False:
            raise Exception(
                "A snapshot with that name exists already. If you wish to continue, add --update."
            )

        print(f"Pausing space: {space_name}")
        self.pause(space_name=space_name)

        try:
            subprocess.call(
                [
                    "rsync",
                    "-r",
                    volume_directory + "/",
                    snapshot_directory + "/",
                    "--update",
                ]
            )
            if not existed:
                self._snapshot_controller.add_snapshot(snapshot_name)

        except Exception as e:
            raise e
        finally:
            print(f"Resuming space: {space_name}")
            self.resume(space_name=space_name)

    def delete_snapshot(self, snapshot_name):
        snapshot_directory = self.get_snapshot_directory(snapshot_name=snapshot_name)
        shutil.rmtree(snapshot_directory)
        self._snapshot_controller.delete_snapshot(snapshot_name)

    def create_from_snapshot(
        self,
        snapshot_name: str,
        space_name: str,
        expose_port: int,
        flavour: str,
        database_name: str,
    ):
        snapshot_dir = self.get_snapshot_directory(snapshot_name)
        print(f"Copying snapshot HD to {snapshot_dir}")
        volume_directory = self.get_volume_directory_for_space(space_name=space_name)
        subprocess.call(["rsync", "-r", snapshot_dir + "/", volume_directory + "/"])
        print("Booting container.")
        self.create(
            space_name=space_name,
            expose_port=expose_port,
            flavour=flavour,
            initial_database=database_name,
        )

    def duplicate_snapshot(self, from_name: str, to_name: str):
        print(f"Copying snapshot from {from_name} to {to_name}")
        from_dir = self.get_snapshot_directory(from_name)
        to_dir = self.get_snapshot_directory(to_name)
        subprocess.call(["rsync", "-r", from_dir + "/", to_dir + "/"])
        self._snapshot_controller.add_snapshot(to_name)
