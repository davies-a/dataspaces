#! /usr/bin/env python3

from pprint import pprint

import click

from dspace.controller import DSpaceController

controller = DSpaceController()


@click.group()
def cli():
    """
    Dataspace is a tool to create ephemeral databases for use in development.

    """
    pass


@cli.command()
def setup():
    """
    Bootstrap a new dspace environment - ensure that requirements are available
    and that configuration has been set up.

    """
    controller.setup()


@cli.command()
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
    default="public",
    help="Initial database to bootstrap for the dataspace. Default: public",
)
def create(name: str, flavour: str, expose_port: int, initial_database: str):
    """
    Create a new dataspace environment.

    """
    controller.create(
        space_name=name,
        expose_port=expose_port,
        flavour=flavour,
        initial_database=initial_database,
    )


@cli.command()
@click.argument("NAME")
@click.option("--snapshot_name", help="Name for the snapshot")
def snapshot(name, snapshot_name):
    """
    Create a snapshot of the dataspace.

    """


@cli.command()
@click.argument("NAME")
@click.option("--tool", default="liquibase", help="Migration tool to use")
@click.option("--folder", help="Folder to read migrations from")
def migrate(name, tool, folder):
    """
    Run database migrations against the dataspace

    """


@cli.command()
@click.argument("NAME")
@click.option("--to", help="Snapshot to roll back to")
def rollback(name, to):
    """
    Roll back to a previous snapshot of the database
    """


@cli.command()
@click.argument("NAME")
def list_snapshots(name):
    """
    List snapshots that exist for the dataspace.
    """


@cli.command()
@click.argument("FROM_NAME")
@click.argument("TO_NAME")
def copy(from_name, to_name):
    """
    Duplicate the dataspace to a new throwaway container
    """


@cli.command()
@click.argument("NAME")
def kill(name):
    """
    Kill and remove the dataspace.

    """
    controller.kill(space_name=name)


@cli.command()
@click.argument("NAME")
def pause(name):
    """
    Pause the dataspace.
    """
    controller.pause(space_name=name)


@cli.command()
@click.argument("NAME")
def resume(name):
    """
    Resume a paused dataspace
    """
    controller.resume(space_name=name)


@cli.command()
@click.option(
    "--active-only/--all", default=False, help="Only show running dataspaces."
)
def ls(active_only: bool):
    """
    List all active and paused dataspaces
    """
    dspaces = controller.list_dataspaces(active_only=active_only)
    for dspace in dspaces:
        dspace_repr = dict(
            Name=dspace.attrs["Name"],
            Image=dspace.attrs["Config"]["Image"],
            State=dspace.attrs["State"]["Status"],
        )
        print(dspace_repr)


@cli.command()
def killall():
    """
    Kill all running and stopped dataspaces
    """
    controller.killall()


if __name__ == "__main__":
    cli()
