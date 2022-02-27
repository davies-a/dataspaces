import click

from .dspace import DSpaceRouter
from .migration import MigrationRouter
from .snapshot import SnapshotRouter


@click.group()
def cli():
    """
    Dataspace is a tool to create ephemeral databases for use in development.

    """
    pass


routers = [DSpaceRouter, SnapshotRouter, MigrationRouter]

for router in routers:
    for command in dir(router):
        if not command.startswith("_"):
            cli.command()(getattr(router, command))
