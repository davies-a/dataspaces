from dspace.flavours.base import Flavour
from dspace.flavours.mysql import MySQLFlavour
from dspace.flavours.postgres import PostgresFlavour

flavours = [
    PostgresFlavour,
    MySQLFlavour,
]

flavour_map = {flavour.name: flavour for flavour in flavours}
