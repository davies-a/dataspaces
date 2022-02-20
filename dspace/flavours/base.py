from abc import ABC
from typing import Dict, List


class Flavour(ABC):
    """
    Database flavour configuration

    """

    name: str

    container_image: str

    connector_port: int

    database_schema: str
    initial_user_variable: str
    initial_password_variable: str
    initial_database_variable: str

    environment_variables: Dict = {}

    healthcheck_command: List[str]

    repl_command: str
