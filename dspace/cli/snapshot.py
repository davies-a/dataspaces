import click

from dspace.cli.base import RouterBase
from dspace.controller import DSpaceController


class SnapshotRouter(RouterBase):
    @staticmethod
    @click.option("--snapshot_name", help="Name for the snapshot")
    @click.option("--update", is_flag=True, help="Update an existing snapshot.")
    @click.argument("SPACE_NAME")
    def snapshot(snapshot_name, space_name, update):
        """
        Create a snapshot of the dataspace.

        """
        DSpaceController().make_snapshot(snapshot_name, space_name, update)

    @staticmethod
    def list_snapshots():
        """
        List snapshots that exist for the dataspace.
        """
        print(DSpaceController()._snapshot_controller.get_snapshots())

    @staticmethod
    @click.argument("FROM_NAME")
    @click.argument("TO_NAME")
    def copy_snapshot(from_name: str, to_name: str):
        DSpaceController().duplicate_snapshot(from_name=from_name, to_name=to_name)

    @staticmethod
    @click.argument("SNAPSHOT_NAME")
    @click.argument("SPACE_NAME")
    @click.option(
        "--flavour", default="postgres", help="Database flavour. Default: postgres"
    )
    @click.option(
        "--expose-port",
        default=5432,
        help="Port to expose the database on from the host. Default: 5423",
    )
    @click.option(
        "--database-name",
        default="db",
        help="Initial database to bootstrap for the dataspace. Default: db",
    )
    def copy_snapshot(snapshot_name, space_name, expose_port, flavour, database_name):
        DSpaceController().create_from_snapshot(
            snapshot_name=snapshot_name,
            space_name=space_name,
            expose_port=expose_port,
            flavour=flavour,
            database_name=database_name,
        )
