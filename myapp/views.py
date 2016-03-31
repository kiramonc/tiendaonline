# coding=utf-8
from pyramid.response import Response
from pyramid.renderers import render
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.view import (view_config,forbidden_view_config)
from pyramid.security import (remember,forget,)
from .models import ( # el nombre de la clase en modelo
    DBSession, Producto, Usuario, Pedido, Prod_Pedido)


@view_config(route_name='home-client', renderer='templates/client/home.pt', permission='shop')
@view_config(route_name='home-admin', renderer='templates/admin/home.pt', permission='edit')
def home(request):
    username = request.authenticated_userid
    if username is None:
        inicio = request.route_url('login')
        return dict(inicio=inicio, logged_in=request.authenticated_userid)
    else:
        user = DBSession.query(Usuario).filter_by(username=username).one()
        if user.rol == 'admins':
            inicio = request.route_url('home-admin')
            return dict(inicio=inicio, logged_in=request.authenticated_userid)
        else:
            inicio = request.route_url('home-client')
            return dict(inicio=inicio, logged_in=request.authenticated_userid)


@view_config(route_name='error-client', renderer='templates/client/error.pt', permission='shop')
@view_config(route_name='error-admin', renderer='templates/admin/error.pt', permission='edit')
@view_config(route_name='pag-error', renderer='templates/error.pt', permission='all')
@forbidden_view_config()
def error(request):
    username = request.authenticated_userid
    if username is None:
        body = render('templates/error.pt', {}, request=request)
        return Response(body, status='403 Forbidden')
    else:
        user = DBSession.query(Usuario).filter_by(username=username).one()
        if user.rol == 'admins':
            body = render('templates/admin/error.pt', {'logged_in':request.authenticated_userid}, request=request)
            return Response(body, status='403 Forbidden')
        else:
            body = render('templates/client/error.pt', {'logged_in':request.authenticated_userid}, request=request)
            return Response(body, status='403 Forbidden')


@view_config(route_name='list', renderer='templates/admin/list.pt', permission='edit')
@view_config(route_name='productos', renderer='templates/client/productos.pt', permission='shop')
@view_config(route_name='list_prod', renderer='templates/productos.pt', permission='all')
def list_product(request):
    data = DBSession.query(Producto).filter_by(estado=True).all()
    return dict(formData=data, logged_in=request.authenticated_userid)


@view_config(route_name='show', renderer='templates/admin/show.pt', permission='edit')
@view_config(route_name='ver', renderer='templates/client/show.pt', permission='shop')
@view_config(route_name='ver_prod', renderer='templates/show.pt', permission='all')
def show_product(request):
    uid = request.matchdict['uid']
    producto = Producto("", "", 0, 0, "")
    buscar = DBSession.query(Producto).filter_by(nombre=uid).count()
    if buscar != 0:
        producto = DBSession.query(Producto).filter_by(nombre=uid).one()
    else:
        return HTTPFound(request.route_url('pag-error'))
    return dict(producto=producto, logged_in=request.authenticated_userid)


@view_config(route_name='register', renderer='templates/register.pt', permission='all')
def register(request):
    message = ''
    if 'form.submitted' in request.params:
        username = request.params['username']
        buscar = DBSession.query(Usuario).filter_by(username=username).count()
        if buscar!=0:
            message = 'Username no disponible, ingrese otro'
        else:
            nombre = request.params['nombre']
            apellido = request.params['apellido']
            password = request.params['password']
            user = Usuario(nombre, apellido, username, password, 'clients', True)
            DBSession.add(user)
            return HTTPFound(request.route_url('login'))

    save_form = request.route_url('register')
    return dict(message=message, save_form=save_form, logged_in=request.authenticated_userid)


@view_config(route_name='login', renderer='templates/login.pt', permission='all')
def login(request):
    login_url = request.route_url('login')
    referrer = request.url

    came_from = request.params.get('came_from', referrer)
    message = ''
    login = ''
    password = ''
    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']
        buscar = DBSession.query(Usuario).filter_by(username=login, estado=True).count()
        if buscar != 0:
            usuario = DBSession.query(Usuario).filter_by(username=login, estado=True).one()
            if usuario.password == password:
                headers = remember(request, login)
                if referrer == login_url:
                    user = DBSession.query(Usuario).filter_by(username=login).one()
                    if user.rol == 'admins':
                        return HTTPFound(request.route_url('home-admin'), headers=headers)
                    else:
                        return HTTPFound(request.route_url('home-client'), headers=headers)

                return HTTPFound(location=came_from, headers=headers)
        message = 'Usuario o password incorrecto'
    return dict(message=message, url=request.route_url('login'), came_from=came_from,
        login = login, password = password)


@view_config(route_name='logout', permission='all')
def logout(request):
    headers = forget(request)
    return HTTPFound(location=request.route_url('login'), headers=headers)


conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_MyApp_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""