# coding=utf-8
from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from sqlalchemy import engine_from_config

from .security import groupfinder
from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')    # motor de base de datos
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    authn_policy = AuthTktAuthenticationPolicy(
        'sosecret', callback=groupfinder, hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(settings=settings, root_factory='.models.RootFactory')
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    # add_route es el "nombre_de_la_vista", "url"
    config.add_route('pag-error', '/error')   # para el inicio de la app
    config.add_route('error-admin', '/error-admin')   # para el inicio de la app
    config.add_route('error-client', '/error-client')   # para el inicio de la app
    config.add_route('home', '/')   # para el inicio de la app
    config.add_route('home-admin', '/admin')   # para el inicio de la app
    config.add_route('home-client', '/client')   # para el inicio de la app
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('add', '/add')   # para agregar un nuevo producto
    config.add_route('list', '/product')        # para ver el listado de productos
    config.add_route('show', '/product/{uid}')  # para ver el detalle de un producto
    config.add_route('edit', '/product/{uid}/edit')  # para editar el producto
    config.add_route('delete', '/product/{uid}/delete')  # para eliminar el producto
    config.add_route('add_user', '/add-user')
    config.add_route('list_user', '/user')
    config.add_route('register', '/register')
    config.add_route('edit_user', '/user/{uid}/edit')
    config.add_route('delete_user', '/user/{uid}/delete')

    config.add_route('productos', '/products')        # para ver el listado de productos
    config.add_route('ver', '/products/{uid}')  # para ver el detalle de un producto
    config.add_route('pedidos', '/pedidos')        # para ver el listado de productos
    config.add_route('detalle_pedido', '/pedidos/{uid}/detalle')        # para ver el listado de productos
    config.add_route('admin_pedidos', '/admin-pedidos')        # para ver el listado de productos
    config.add_route('detalle_pedido_admin', '/pedidos/{uid}/admin')        # para ver el listado de productos
    config.add_route('cuenta', '/my-account')        # para ver el listado de productos
    config.add_route('desactivar', '/desc-account')   # para ver el listado de productos
    config.add_route('carrito', '/chart')        # para ver el listado de productos
    config.add_route('list_prod', '/productos')        # para ver el listado de productos
    config.add_route('ver_prod', '/productos/{uid}')  # para ver el detalle de un producto

    config.add_route('generate_ajax_data', '/ajax_view')
    config.add_route('get_data', '/pedido_data/{uid}')

    config.scan()
    return config.make_wsgi_app()
