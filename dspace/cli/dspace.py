import click

from dspace.cli.base import RouterBase
from dspace.controller import DSpaceController


class DSpaceRouter(RouterBase):
    @staticmethod
    def setup():
        """
        Bootstrap a new dspace environment - ensure that requirements are available
        and that configuration has been set up.

        """
        DSpaceController.setup()

    @staticmethod
    @click.option("--name", default="db", help="Name for the container. Default: db.")
    @click.option(
        "--flavour", default="postgres", help="Database flavour. Default: postgres"
    )
    @click.option(
        "--expose-port",
        default=5432,
        help="Port to expose the database on from the host. Default: 5423",
    )
    @click.option(
        "--initial-database",
        default="db",
        help="Initial database to bootstrap for the dataspace. Default: db",
    )
    def create(name: str, flavour: str, expose_port: int, initial_database: str):
        """
        Create a new dataspace environment.

        """
        DSpaceController().create(
            space_name=name,
            expose_port=expose_port,
            flavour=flavour,
            initial_database=initial_database,
        )

    @staticmethod
    @click.argument("NAME")
    def kill(name):
        """
        Kill and remove the dataspace.

        """
        DSpaceController().kill(space_name=name)

    @staticmethod
    @click.argument("FROM_NAME")
    @click.argument("TO_NAME")
    def copy(from_name, to_name):
        """
        Duplicate the dataspace to a new throwaway container
        TODO: Implement
        """

    @staticmethod
    @click.argument("NAME")
    def pause(name):
        """
        Pause the dataspace.
        """
        DSpaceController().pause(space_name=name)

    @staticmethod
    @click.argument("NAME")
    def resume(name):
        """
        Resume a paused dataspace
        """
        DSpaceController().resume(space_name=name)

    @staticmethod
    @click.option(
        "--active-only/--all", default=False, help="Only show running dataspaces."
    )
    def ls(active_only: bool):
        """
        List all active and paused dataspaces
        """
        dspaces = DSpaceController().list_dataspaces(active_only=active_only)
        for dspace in dspaces:
            dspace_repr = dict(
                Name=dspace.attrs["Name"],
                Image=dspace.attrs["Config"]["Image"],
                State=dspace.attrs["State"]["Status"],
            )
            print(dspace_repr)

    @staticmethod
    def killall():
        """
        Kill all running and stopped dataspaces
        """
        DSpaceController().killall()

    @staticmethod
    @click.argument("NAME")
    def shell(name):
        """
        Open an interactive Bash shell in the space
        """
        DSpaceController().spawn_shell(space_name=name)

    @staticmethod
    @click.argument("NAME")
    def dba(name):
        """
        Open an interactive database REPL.
        """
        DSpaceController().dba(space_name=name)

    @staticmethod
    @click.argument("NAME")
    @click.option("--to", help="Snapshot to roll back to")
    def rollback(name, to):
        """
        Roll back to a previous snapshot of the database
        TODO: Implement
        """
