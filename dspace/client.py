import docker


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

    def create_container(
        self,
        name: str,
        expose_port: int,
        container_image: str,
        initial_database: str,
        initial_user: str,
        initial_password: str,
    ):
        self.client.containers.run(
            container_image,
            detach=True,
            labels=["DSPACE"],
            name=name,
            network=self.dspace_network_name,
            ports={"5432/tcp": expose_port},
            environment={
                "POSTGRES_DB": initial_database,
                "POSTGRES_USER": initial_user,
                "POSTGRES_PASSWORD": initial_password.get_secret_value(),
            },
        )

    def kill_container(self, name: str):
        container = self.client.containers.get(name)
        container.remove(force=True)

    def pause_container(self, name: str):
        container = self.client.containers.get(name)
        container.pause()

    def resume_container(self, name: str):
        container = self.client.containers.get(name)
        container.unpause()

    def list_containers(self, active_only):
        containers = self.client.containers.list(
            all=not active_only, filters={"label": "DSPACE"}
        )

        return containers

    def killall(self):
        for container in self.list_containers(active_only=False):
            self.kill_container(container.id)
