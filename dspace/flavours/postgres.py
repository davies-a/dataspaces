from dspace.flavours.base import Flavour

class PostgresFlavour(Flavour):
    """
    Postgres Database flavour

    """
    name = 'postgres'

    container_image = 'postgres:14'

    connector_port = 5432

    database_schema = 'postgresql'
    initial_user_variable = 'POSTGRES_USER'
    initial_password_variable = 'POSTGRES_DB'
    initial_database_variable = 'POSTGRES_PASSWORD'

    healthcheck_command = ["pg_isready"]
