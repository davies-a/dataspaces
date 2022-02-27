import click

from dspace.cli.base import RouterBase


class MigrationRouter(RouterBase):
    @staticmethod
    @click.argument("NAME")
    @click.option("--tool", default="liquibase", help="Migration tool to use")
    @click.option("--folder", help="Folder to read migrations from")
    def migrate(name, tool, folder):
        """
        Run database migrations against the dataspace

        TODO: Implement

        """
