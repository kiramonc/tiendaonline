# coding=utf-8
import os
import sys
import transaction

from sqlalchemy import engine_from_config
from sqlalchemy import create_engine
from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

# from pyramid.scripts.common import parse_vars

from ..models import (
    DBSession,
    Producto,  # el nombre de la clase en modelo
    Usuario,
    Pedido,
    Prod_Pedido,
    Base,
)


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    # options = parse_vars(argv[2:])
    setup_logging(config_uri)
    # settings = get_appsettings(config_uri, options=options)
    # settings = get_appsettings(config_uri)
    # engine = engine_from_config(settings, 'sqlalchemy.')
    engine = create_engine('postgresql://admintienda:admintienda@localhost:5432/tiendaonlinedb')

    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        model = Producto(nombre='ejemplo', descripcion="test", inventario=8, precio=12.08, img='ejemplo.png')
        model1 = Usuario(username='admin', password='admin123', nombre='Katherine', apellido='Ramon', rol='admins')
        model2 = Usuario(username='cliente', password='cliente', nombre='Katherine', apellido='Ramon', rol='clients')
        DBSession.add(model)
        DBSession.add(model1)
        DBSession.add(model2)
