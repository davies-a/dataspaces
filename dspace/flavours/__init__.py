from dspace.flavours.base import Flavour
from dspace.flavours.postgres import PostgresFlavour
from dspace.flavours.mysql import MySQLFlavour

flavours = [
    PostgresFlavour,
    MySQLFlavour,
]

flavour_map = {flavour.name: flavour for flavour in flavours}
