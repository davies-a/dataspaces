from dspace.flavours.base import Flavour


class MySQLFlavour(Flavour):
    name = "mysql"

    container_image = "mysql:5.7"

    connector_port = 3306

    database_schema = "mysql"

    initial_user_variable = "MYSQL_USER"
    initial_password_variable = "MYSQL_PASSWORD"
    initial_database_variable = "MYSQL_DATABASE"

    environment_variables = {
        "MYSQL_RANDOM_ROOT_PASSWORD": "yes",
    }

    healthcheck_command = [
        "mysqladmin ping --host=localhost --user=${MYSQL_USER} --password=${MYSQL_PASSWORD} --silent"
    ]

    repl_command = (
        "'mysql -u${MYSQL_USER} -p${MYSQL_PASSWORD} -h localhost -D${MYSQL_DATABASE}'"
    )

    volume_directory = "/var/lib/mysql"
