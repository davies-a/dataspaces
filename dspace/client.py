import docker

from dspace.flavours.base import Flavour


class DockerClient:
    dspace_network_name = "dspace"

    client = docker.from_env()

    def create_network(self):
        """
        Create a docker network for dataspaces.

        """
        self.client.networks.create(self.dspace_network_name)

    def ensure_network_exists(self):
        """
        Ensure that a docker network exists for dataspaces to use.

        """
        networks = self.client.networks.list(names=[self.dspace_network_name])
        if not networks:
            print("Creating a network for dspaces...")
            self.create_network()
        else:
            print("A docker network for dspace already exists.")

    def get_container(self, name: str):
        return self.client.containers.get(name)

    def list_containers(self, active_only):
        containers = self.client.containers.list(
            all=not active_only, filters={"label": "DSPACE"}
        )

        return containers

    def create_container(
        self,
        name: str,
        expose_port: int,
        flavour: Flavour,
        database: str,
        user: str,
        password: str,
    ):
        healthcheck_nanoseconds = 10 * 1000 * 1000 * 1000

        self.client.containers.run(
            flavour.container_image,
            detach=True,
            labels=["DSPACE"],
            name=name,
            network=self.dspace_network_name,
            ports={f"{flavour.connector_port}/tcp": expose_port},
            environment={
                flavour.initial_user_variable: user,
                flavour.initial_database_variable: database,
                flavour.initial_password_variable: password.get_secret_value(),
                **flavour.environment_variables,
            },
            healthcheck={
                "test": ["CMD-SHELL", *flavour.healthcheck_command],
                "interval": healthcheck_nanoseconds,
                "timeout": healthcheck_nanoseconds,
                "retries": 5,
            },
        )

    def kill_container(self, name: str):
        container = self.get_container(name)
        container.remove(force=True)

    def pause_container(self, name: str):
        container = self.get_container(name)
        container.pause()

    def resume_container(self, name: str):
        container = self.get_container(name)
        container.unpause()

    def killall(self):
        for container in self.list_containers(active_only=False):
            self.kill_container(container.id)
